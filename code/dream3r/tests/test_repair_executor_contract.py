"""
Dream3R v0.4 RepairExecutor contract tests.

Validates that the critic -> repair loop is REAL: each action actually
exercises a different control path, max_repair_attempts is honored, and
the repair_action_log records every attempt.

These tests bypass the critic head's stochastic argmax by injecting
synthetic CriticDecision objects directly into the executor.
"""

import os
import sys

import torch

HERE = os.path.dirname(os.path.abspath(__file__))
CODE_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
if CODE_ROOT not in sys.path:
    sys.path.insert(0, CODE_ROOT)

from dream3r.contracts import CriticDecision, REPAIR_ACTION_NAMES
from dream3r.model import build_dream3r
from dream3r.orchestrator import build_v04_pipeline
from dream3r.repair import RepairExecutor


def _make_pipeline(max_attempts: int = 1):
    torch.manual_seed(123)
    model = build_dream3r("small")
    pipeline = build_v04_pipeline(model, max_repair_attempts=max_attempts)
    feats = torch.randn(1, 2, 17, 768)
    imgs = torch.randn(1, 2, 3, 64, 64)
    return pipeline, feats, imgs


def _synthetic_decision(action: int, batch: int = 1) -> CriticDecision:
    return CriticDecision(
        conflict_score=torch.zeros(batch, 1),
        repair_action=torch.full((batch,), action, dtype=torch.long),
        reroute_hint=torch.tensor([action == 3] * batch),
        reason_codes=[["synthetic"]] * batch,
        local_window_ids=[0],
        critic_log={},
    )


def test_action_zero_is_noop_and_logs_clean_attempt():
    pipeline, feats, imgs = _make_pipeline()
    pipeline.repair.begin_call()
    primary = pipeline._call_model(
        x=feats, regime_probs=None, prev_memory_state=None,
        prev_object_slots=None, prev_object_slot_poses=None, timestep=0,
    )
    decision = _synthetic_decision(0)
    out = pipeline.repair.execute(
        primary, decision,
        forward_fn=pipeline._call_model,
        forward_kwargs={
            "x": feats, "regime_probs": None, "prev_memory_state": None,
            "prev_object_slots": None, "prev_object_slot_poses": None,
            "timestep": 0,
        },
    )
    assert out is primary
    report = pipeline.repair.finalize()
    assert report.final_action == 0
    assert report.n_attempts == 0
    assert report.capped is False
    assert len(report.attempts) == 1
    assert report.attempts[0].action_name == "no_repair"


def test_action_one_triggers_real_local_rerun():
    pipeline, feats, imgs = _make_pipeline(max_attempts=1)
    pipeline.repair.begin_call()
    primary = pipeline._call_model(
        x=feats, regime_probs=None, prev_memory_state=None,
        prev_object_slots=None, prev_object_slot_poses=None, timestep=0,
    )
    decision = _synthetic_decision(1)
    new = pipeline.repair.execute(
        primary, decision,
        forward_fn=pipeline._call_model,
        forward_kwargs={
            "x": feats, "regime_probs": None, "prev_memory_state": None,
            "prev_object_slots": None, "prev_object_slot_poses": None,
            "timestep": 0,
        },
    )
    assert new is not primary, "local rerun must return a fresh forward dict"
    assert (new["pointmap"] - primary["pointmap"]).abs().max().item() > 0
    report = pipeline.repair.finalize()
    assert report.final_action == 1
    assert report.n_attempts == 1
    succeeded = [a for a in report.attempts if a.succeeded]
    assert any(a.action_name == "local_rerun" for a in succeeded)


def test_action_two_triggers_window_rerun_and_respects_max_attempts():
    pipeline, feats, imgs = _make_pipeline(max_attempts=1)
    pipeline.repair.begin_call()
    forward_kwargs = {
        "x": feats, "regime_probs": None, "prev_memory_state": None,
        "prev_object_slots": None, "prev_object_slot_poses": None,
        "timestep": 0,
    }
    primary = pipeline._call_model(**forward_kwargs)

    # First call: should rerun and count one attempt.
    new = pipeline.repair.execute(primary, _synthetic_decision(2),
                                  forward_fn=pipeline._call_model,
                                  forward_kwargs=forward_kwargs)
    assert new is not primary
    assert (new["pointmap"] - primary["pointmap"]).abs().max().item() > 0

    # Second call within the same call-window: cap should kick in and
    # return the latest output without another rerun.
    capped_out = pipeline.repair.execute(new, _synthetic_decision(2),
                                          forward_fn=pipeline._call_model,
                                          forward_kwargs=forward_kwargs)
    assert capped_out is new, "max_repair_attempts must prevent a second rerun"

    report = pipeline.repair.finalize()
    assert report.max_attempts == 1
    assert report.n_attempts == 1
    assert report.capped is True
    cap_msgs = [a for a in report.attempts if not a.succeeded and a.action_code == 2]
    assert cap_msgs, "capped attempt must appear in the log"


def test_action_three_sets_reroute_hint_without_rerun():
    pipeline, feats, imgs = _make_pipeline()
    pipeline.repair.begin_call()
    forward_kwargs = {
        "x": feats, "regime_probs": None, "prev_memory_state": None,
        "prev_object_slots": None, "prev_object_slot_poses": None,
        "timestep": 0,
    }
    primary = pipeline._call_model(**forward_kwargs)
    new = pipeline.repair.execute(primary, _synthetic_decision(3),
                                  forward_fn=pipeline._call_model,
                                  forward_kwargs=forward_kwargs)
    # Action 3 must NOT rerun the model — the orchestrator handles the
    # reroute via the Composer instead.
    assert new is primary
    report = pipeline.repair.finalize()
    assert report.reroute_hint is True
    assert report.n_attempts == 0
    assert any(a.action_name == "reroute_model" for a in report.attempts)


def test_repair_executor_does_not_loop_forever_when_actions_persist():
    pipeline, feats, imgs = _make_pipeline(max_attempts=2)
    pipeline.repair.begin_call()
    forward_kwargs = {
        "x": feats, "regime_probs": None, "prev_memory_state": None,
        "prev_object_slots": None, "prev_object_slot_poses": None,
        "timestep": 0,
    }
    primary = pipeline._call_model(**forward_kwargs)
    last = primary
    for _ in range(5):
        last = pipeline.repair.execute(last, _synthetic_decision(1),
                                       forward_fn=pipeline._call_model,
                                       forward_kwargs=forward_kwargs)
    report = pipeline.repair.finalize()
    assert report.n_attempts == 2  # bounded by max_attempts=2
    assert report.capped is True


def test_repair_action_log_is_present_in_reconstruction_output():
    pipeline, feats, imgs = _make_pipeline()
    out = pipeline(images=imgs, features=feats)
    log = out.repair_action_log
    assert "final_action" in log
    assert "final_action_name" in log
    assert log["final_action_name"] in REPAIR_ACTION_NAMES.values()
    assert "attempts" in log
    assert "implemented_actions" in log
    assert set(log["implemented_actions"]) == set(REPAIR_ACTION_NAMES.keys())


if __name__ == "__main__":
    test_action_zero_is_noop_and_logs_clean_attempt()
    test_action_one_triggers_real_local_rerun()
    test_action_two_triggers_window_rerun_and_respects_max_attempts()
    test_action_three_sets_reroute_hint_without_rerun()
    test_repair_executor_does_not_loop_forever_when_actions_persist()
    test_repair_action_log_is_present_in_reconstruction_output()
    print("RepairExecutor contract tests: PASS")
