"""
Dream3R v0.4 RepairExecutor — closes the critic -> repair loop.

The v0.3 model.py already wired the bus so that a previous-tick
recommended_action influences Memory retrieval depth (CR-3 boost when
action==1) and Composer confidence (zeroed when action==2). What it did
NOT do was actually invoke a corrective rerun. The Critic published a
recommendation and the pipeline moved on.

RepairExecutor closes that loop:

  action=0 no_repair:    pass through; record noop in log.
  action=1 local_rerun:  re-run model.forward once with action=1 injected
                         into the bus's previous_signals (so Memory raises
                         CR-3 retrieval depth and Composer sees a low-conf
                         budget). Counts as one attempt.
  action=2 window_rerun: re-run model.forward fresh (state reset) with
                         action=2 injected. Capped at max_repair_attempts
                         (default 1) so we cannot loop forever even if the
                         second forward still flags a conflict.
  action=3 reroute_model: do NOT rerun model; instead emit reroute_hint=True
                         so the orchestrator picks the second-best expert
                         from Composer route_recommendation.

Every entry — no_repair, real rerun, capped rerun, and reroute — appears in
RepairReport.attempts so downstream callers can audit the closed loop.
"""

from typing import Any, Callable, Dict, List, Optional

import torch

from dream3r.bus import EvidenceLabel
from dream3r.contracts import (
    REPAIR_ACTION_NAMES,
    CriticDecision,
    RepairAttempt,
    RepairReport,
)


class RepairExecutor:
    """Owns the critic -> rerun feedback loop.

    Stateful per pipeline.forward call: ``begin_call`` resets attempt
    counters; ``execute`` is invoked once with the critic decision; results
    are reported via ``finalize`` which returns a RepairReport.

    Args:
        model:                Dream3R instance whose forward we may rerun.
        max_repair_attempts:  upper bound on how many real reruns are allowed
                              in a single pipeline.forward call. Default 1
                              keeps the loop bounded; raising it should be
                              done carefully because each rerun re-touches
                              the bus + memory state.
    """

    def __init__(self, model, max_repair_attempts: int = 1):
        self.model = model
        self.max_repair_attempts = int(max_repair_attempts)
        self._attempts: List[RepairAttempt] = []
        self._n_real_attempts = 0
        self._capped = False
        self._reroute_hint = False
        self._final_action = 0

    # ---------- lifecycle ----------

    def begin_call(self) -> None:
        self._attempts = []
        self._n_real_attempts = 0
        self._capped = False
        self._reroute_hint = False
        self._final_action = 0

    def finalize(self) -> RepairReport:
        return RepairReport(
            final_action=self._final_action,
            final_action_name=REPAIR_ACTION_NAMES.get(self._final_action, "unknown"),
            n_attempts=self._n_real_attempts,
            max_attempts=self.max_repair_attempts,
            reroute_hint=self._reroute_hint,
            attempts=list(self._attempts),
            capped=self._capped,
        )

    # ---------- execution ----------

    def execute(self,
                primary_output: Dict[str, torch.Tensor],
                critic_decision: CriticDecision,
                forward_fn: Callable[..., Dict[str, torch.Tensor]],
                forward_kwargs: Dict[str, Any],
                ) -> Dict[str, torch.Tensor]:
        """Apply the critic decision and return the (possibly updated) raw forward.

        Args:
            primary_output: the dict returned by the first model.forward call.
            critic_decision: CriticDecision built from primary_output.
            forward_fn: callable that triggers another model.forward (the
                orchestrator passes a thin closure so we do not need to
                know the model's exact arg names).
            forward_kwargs: kwargs forwarded to forward_fn for a rerun.

        Returns:
            either the original primary_output (action 0 / 3) or a new
            forward dict (action 1 / 2). The orchestrator chooses which
            to use downstream.
        """
        action = int(critic_decision.repair_action.max().item())
        self._final_action = action

        if action <= 0:
            self._record(0, "critic_clean", "no repair requested", True, True, "")
            return primary_output

        if action == 1:
            return self._local_rerun(primary_output, forward_fn, forward_kwargs)

        if action == 2:
            return self._window_rerun(primary_output, forward_fn, forward_kwargs)

        if action == 3:
            self._reroute_hint = True
            self._record(3, "critic_reroute",
                         "reroute_hint=True; orchestrator selects alternative expert",
                         True, True, "no model rerun for action=3")
            return primary_output

        # Any unknown action falls back to no_repair so a stub action code
        # never triggers an unbounded loop.
        self._record(action, "unknown_action",
                     "action code not recognized — treating as no_repair",
                     True, False, "")
        self._final_action = 0
        return primary_output

    # ---------- private helpers ----------

    def _local_rerun(self, primary_output, forward_fn, forward_kwargs):
        if self._n_real_attempts >= self.max_repair_attempts:
            self._capped = True
            self._record(1, "critic_local_rerun",
                         "local rerun requested but max_repair_attempts reached",
                         True, False, "cap hit; returning primary output")
            return primary_output

        self._inject_previous_action(1)
        try:
            new_output = forward_fn(**forward_kwargs)
            self._n_real_attempts += 1
            self._record(1, "critic_local_rerun",
                         "rerun model with action=1 to deepen Memory retrieval",
                         True, True, "")
            return new_output
        except Exception as exc:  # noqa: BLE001 — surface failure into log, do not crash pipeline
            self._record(1, "critic_local_rerun",
                         f"rerun raised {type(exc).__name__}: {exc}",
                         True, False, "fallback to primary output")
            return primary_output

    def _window_rerun(self, primary_output, forward_fn, forward_kwargs):
        if self._n_real_attempts >= self.max_repair_attempts:
            self._capped = True
            self._record(2, "critic_window_rerun",
                         "window rerun requested but max_repair_attempts reached",
                         True, False, "cap hit; returning primary output")
            return primary_output

        rerun_kwargs = dict(forward_kwargs)
        rerun_kwargs["prev_memory_state"] = None
        rerun_kwargs["prev_object_slots"] = None
        rerun_kwargs["prev_object_slot_poses"] = None

        self._inject_previous_action(2)
        try:
            new_output = forward_fn(**rerun_kwargs)
            self._n_real_attempts += 1
            self._record(2, "critic_window_rerun",
                         "full window rerun with cleared memory + slots; action=2 injected",
                         True, True, "")
            return new_output
        except Exception as exc:  # noqa: BLE001
            self._record(2, "critic_window_rerun",
                         f"rerun raised {type(exc).__name__}: {exc}",
                         True, False, "fallback to primary output")
            return primary_output

    def _inject_previous_action(self, action_code: int) -> None:
        """Publish a synthetic recommended_action so the next forward sees it.

        Dream3R.forward calls self.bus.reset() as its first step, which
        moves current _signals into _previous_signals. By publishing a
        critic-owned recommended_action here we guarantee that the rerun's
        Memory + Composer branches read action_code as the prior tick's
        repair recommendation.
        """
        bus = getattr(self.model, "bus", None)
        if bus is None:
            return
        device = next(self.model.parameters()).device
        try:
            B = self.model.bus._signals.get("conflict_score").tensor.shape[0]
        except Exception:
            B = 1
        tensor = torch.full((B, 1), float(action_code), device=device)
        bus.publish("recommended_action", tensor,
                    EvidenceLabel.INFERRED, "critic", timestep=-1)

    def _record(self, action_code: int, reason: str, note: str,
                triggered_by_critic: bool, succeeded: bool,
                extra_note: str) -> None:
        self._attempts.append(RepairAttempt(
            attempt_index=len(self._attempts),
            action_code=action_code,
            action_name=REPAIR_ACTION_NAMES.get(action_code, f"action_{action_code}"),
            reason=reason,
            triggered_by_critic=triggered_by_critic,
            succeeded=succeeded,
            note=f"{note}; {extra_note}" if extra_note else note,
        ))
