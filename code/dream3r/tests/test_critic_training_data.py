"""Schema tests for Stage 4 critic training data helpers."""

from dream3r.scripts.build_critic_training_data import _action_for


def test_action_for_clean_output_uses_no_repair():
    assert _action_for(0.1, 0.3, conflict_threshold=0.2, reroute_margin=0.01) == 0


def test_action_for_bad_output_uses_reroute_when_alternative_is_better():
    assert _action_for(0.4, 0.2, conflict_threshold=0.2, reroute_margin=0.01) == 3


def test_action_for_bad_output_uses_offpath_when_no_alternative_improves():
    assert _action_for(0.4, 0.395, conflict_threshold=0.2, reroute_margin=0.01) == 4
