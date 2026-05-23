"""Tests for A8: Memory A1 sub-action policy and TTT state updater."""

import pytest
import torch

from dream3r.memory_action import (
    MemoryA1Action,
    A1_ACTION_NAMES,
    A1PolicyDecision,
    StateUpdatePolicy,
    TTTStateUpdater,
)


class TestMemoryA1ActionEnum:
    def test_enum_has_6_actions(self):
        assert len(MemoryA1Action) == 6

    def test_action_names_match_spec(self):
        expected = {"full_update", "pose_adaptive_update", "kalman_update",
                    "skip_update", "reset_state", "test_time_train"}
        assert set(A1_ACTION_NAMES.values()) == expected

    def test_ttt_action_is_5(self):
        assert MemoryA1Action.TEST_TIME_TRAIN == 5

    def test_full_update_is_default_zero(self):
        assert MemoryA1Action.FULL_UPDATE == 0


class TestStateUpdatePolicy:
    def setup_method(self):
        self.policy = StateUpdatePolicy(n_actions=6, d_input=4, d_hidden=32)

    def test_forward_returns_list_of_decisions(self):
        B = 3
        decisions = self.policy(
            drift_proxy=torch.randn(B, 1),
            conflict_score=torch.randn(B, 1),
            confidence_mean=torch.rand(B, 1),
            window_index=0,
        )
        assert len(decisions) == B
        assert all(isinstance(d, A1PolicyDecision) for d in decisions)

    def test_decision_fields(self):
        decisions = self.policy(
            drift_proxy=torch.zeros(1, 1),
            conflict_score=torch.zeros(1, 1),
            confidence_mean=torch.ones(1, 1),
            window_index=0,
        )
        d = decisions[0]
        assert isinstance(d.action, MemoryA1Action)
        assert 0.0 <= d.confidence <= 1.0
        assert isinstance(d.reason, str)
        assert d.policy_logits is not None
        assert d.policy_logits.shape == (6,)

    def test_ttt_boost_at_high_drift_long_sequence(self):
        """When drift > threshold and window >= min, TTT action should be boosted."""
        torch.manual_seed(42)
        policy = StateUpdatePolicy(n_actions=6)
        policy.ttt_drift_threshold = 0.3
        policy.ttt_min_window = 5

        # High drift scenario at a late window
        decisions = policy(
            drift_proxy=torch.tensor([[0.8]]),
            conflict_score=torch.tensor([[0.5]]),
            confidence_mean=torch.tensor([[0.3]]),
            window_index=10,
        )
        # With the boost, TTT should be selected (or at least have high logit)
        logits = decisions[0].policy_logits
        ttt_logit = logits[MemoryA1Action.TEST_TIME_TRAIN].item()
        # TTT logit should be boosted by 3.0 relative to no-boost scenario
        assert ttt_logit > logits.mean().item()

    def test_no_ttt_boost_at_early_window(self):
        """TTT boost should NOT activate before min_window."""
        policy = StateUpdatePolicy(n_actions=6)
        policy.ttt_min_window = 8

        decisions_early = policy(
            drift_proxy=torch.tensor([[0.9]]),
            conflict_score=torch.tensor([[0.5]]),
            confidence_mean=torch.tensor([[0.3]]),
            window_index=3,
        )
        decisions_late = policy(
            drift_proxy=torch.tensor([[0.9]]),
            conflict_score=torch.tensor([[0.5]]),
            confidence_mean=torch.tensor([[0.3]]),
            window_index=10,
        )
        # Late window should have higher TTT logit due to boost
        early_ttt = decisions_early[0].policy_logits[MemoryA1Action.TEST_TIME_TRAIN]
        late_ttt = decisions_late[0].policy_logits[MemoryA1Action.TEST_TIME_TRAIN]
        assert late_ttt > early_ttt

    def test_policy_gradient_flows(self):
        policy = StateUpdatePolicy(n_actions=6)
        drift = torch.randn(2, 1, requires_grad=True)
        conflict = torch.randn(2, 1)
        conf = torch.rand(2, 1)

        # Forward through policy net directly for gradient check
        window_feat = torch.zeros(2, 1)
        x = torch.cat([drift, conflict, conf, window_feat], dim=-1)
        logits = policy.policy_net(x)
        loss = logits.sum()
        loss.backward()
        assert drift.grad is not None


class TestTTTStateUpdater:
    def setup_method(self):
        self.updater = TTTStateUpdater(d_state=128, lr=1e-3)

    def test_output_shape_matches_input(self):
        state = torch.randn(2, 32, 128)
        updated = self.updater(state)
        assert updated.shape == state.shape

    def test_update_is_residual(self):
        """Updated state should differ from input (non-identity)."""
        state = torch.randn(1, 16, 128)
        updated = self.updater(state)
        assert not torch.allclose(state, updated, atol=1e-7)

    def test_update_magnitude_is_small(self):
        """The correction should be small (scaled by lr=1e-3)."""
        state = torch.randn(1, 16, 128)
        updated = self.updater(state)
        diff = (updated - state).abs().mean()
        assert diff < 0.1  # Should be much less than state magnitude

    def test_gradient_flows_through_updater(self):
        state = torch.randn(1, 8, 128, requires_grad=True)
        updated = self.updater(state)
        loss = updated.sum()
        loss.backward()
        assert state.grad is not None

    def test_with_frame_tokens(self):
        """Forward should work with optional frame_tokens arg."""
        state = torch.randn(1, 16, 128)
        frame_tokens = torch.randn(1, 4, 196, 128)
        updated = self.updater(state, current_frame_tokens=frame_tokens)
        assert updated.shape == state.shape
