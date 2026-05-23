"""
Memory A1 sub-action vocabulary for Dream3R C2 state-update policy.

Per SPEC-20260503-002 (Memory finalist spec) and SPEC-20260522-001 (v0.5 axes A8),
the Memory module selects among A1 sub-actions at each tick based on evidence signals.

Sub-action selection criteria:
  - evidence_signals from C1 Perception (confidence, spatial coverage)
  - latent_drift_proxy from C2 Memory (state stability indicator)
  - conflict_score from C4 Critic (geometric validation failure rate)

The tttLRM-style sub-action (test_time_train) targets long-sequence regression
by performing gradient-based state update at test time.
"""

from enum import IntEnum
from dataclasses import dataclass, field
from typing import Dict, Optional, List

import torch
import torch.nn as nn


class MemoryA1Action(IntEnum):
    """A1 sub-action codes per SPEC-20260503-002."""
    FULL_UPDATE = 0           # Standard full state update (default)
    POSE_ADAPTIVE_UPDATE = 1  # PAS3R-style: scale update by pose change
    KALMAN_UPDATE = 2         # FILT3R-style: Kalman latent filtering
    SKIP_UPDATE = 3           # No state update this tick (frozen state)
    RESET_STATE = 4           # Hard reset state to initial
    TEST_TIME_TRAIN = 5       # tttLRM-style: gradient-based long-context update


A1_ACTION_NAMES = {int(a): a.name.lower() for a in MemoryA1Action}


@dataclass
class A1PolicyDecision:
    """Result of the state-update policy selection."""
    action: MemoryA1Action
    confidence: float = 1.0
    reason: str = ""
    policy_logits: Optional[torch.Tensor] = None  # [n_actions]


class StateUpdatePolicy(nn.Module):
    """
    Selects among A1 sub-actions based on evidence signals.

    Inputs:
        drift_proxy:      [B, 1] latent drift from memory module
        conflict_score:   [B, 1] from C4 Critic
        confidence_mean:  [B, 1] mean perception confidence
        window_index:     int    current tick index in sequence

    Output:
        A1PolicyDecision per batch element (policy_logits for training)
    """

    def __init__(self, n_actions: int = 6, d_input: int = 4, d_hidden: int = 32):
        super().__init__()
        self.n_actions = n_actions
        self.policy_net = nn.Sequential(
            nn.Linear(d_input, d_hidden),
            nn.GELU(),
            nn.Linear(d_hidden, d_hidden),
            nn.GELU(),
            nn.Linear(d_hidden, n_actions),
        )
        # Threshold for switching to tttLRM-style update
        self.ttt_drift_threshold = 0.4
        self.ttt_min_window = 8  # Only consider TTT after enough windows

    def forward(self, drift_proxy: torch.Tensor,
                conflict_score: torch.Tensor,
                confidence_mean: torch.Tensor,
                window_index: int = 0) -> List[A1PolicyDecision]:
        """
        Select A1 sub-action for each batch element.

        Returns a list of A1PolicyDecision (one per batch element).
        """
        B = drift_proxy.shape[0]
        device = drift_proxy.device

        # Build input features
        window_feat = torch.full((B, 1), float(window_index) / 100.0, device=device)
        x = torch.cat([drift_proxy, conflict_score, confidence_mean, window_feat], dim=-1)

        # Policy network logits
        logits = self.policy_net(x)  # [B, n_actions]

        # Rule-based override: if drift is high and window > threshold, bias toward TTT
        if window_index >= self.ttt_min_window:
            high_drift_mask = (drift_proxy.squeeze(-1) > self.ttt_drift_threshold)
            if high_drift_mask.any():
                ttt_boost = torch.zeros_like(logits)
                ttt_boost[high_drift_mask, MemoryA1Action.TEST_TIME_TRAIN] = 3.0
                logits = logits + ttt_boost

        # Softmax for training; argmax for inference
        probs = torch.softmax(logits, dim=-1)
        actions = logits.argmax(dim=-1)

        decisions = []
        for b in range(B):
            action_code = MemoryA1Action(actions[b].item())
            decisions.append(A1PolicyDecision(
                action=action_code,
                confidence=probs[b, actions[b]].item(),
                reason=self._reason(action_code, drift_proxy[b].item(),
                                    conflict_score[b].item(), window_index),
                policy_logits=logits[b].detach(),
            ))
        return decisions

    def _reason(self, action: MemoryA1Action, drift: float,
                conflict: float, window: int) -> str:
        if action == MemoryA1Action.TEST_TIME_TRAIN:
            return f"drift={drift:.3f}>thr, window={window}>=min"
        elif action == MemoryA1Action.SKIP_UPDATE:
            return f"low_drift={drift:.3f}, low_conflict={conflict:.3f}"
        elif action == MemoryA1Action.RESET_STATE:
            return f"critical_conflict={conflict:.3f}"
        else:
            return f"default_policy, drift={drift:.3f}"


class TTTStateUpdater(nn.Module):
    """
    tttLRM-style test-time training state updater.

    When the StateUpdatePolicy selects TEST_TIME_TRAIN, this module
    performs a single gradient step on the memory state using a
    self-supervised consistency loss computed from the current window.

    This is a scaffold implementation — the real tttLRM gradient step
    requires the latent state to be detached and re-optimized, which
    is deferred to W25 training integration.
    """

    def __init__(self, d_state: int = 128, lr: float = 1e-3):
        super().__init__()
        self.d_state = d_state
        self.lr = lr
        # Lightweight projection for self-supervised target
        self.target_proj = nn.Linear(d_state, d_state)
        self.predictor = nn.Linear(d_state, d_state)

    def forward(self, state: torch.Tensor,
                current_frame_tokens: Optional[torch.Tensor] = None
                ) -> torch.Tensor:
        """
        Apply one TTT step to the state.

        In scaffold mode, applies a learned projection as a proxy for
        the full gradient-based update. Real implementation (W25) will
        compute loss and backprop through state.

        Args:
            state: [B, S, D] current latent state tokens
            current_frame_tokens: [B, N, P, D] optional frame context

        Returns:
            Updated state [B, S, D]
        """
        # Scaffold: apply a residual update simulating one TTT step
        target = self.target_proj(state.detach())
        prediction = self.predictor(state)
        # Residual correction toward target (proxy for gradient step)
        correction = (target - prediction) * self.lr
        updated_state = state + correction
        return updated_state
