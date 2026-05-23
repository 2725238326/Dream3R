"""
Dream3R configuration system.

Usage:
    from dream3r.config import load_config, PRESETS
    cfg = load_config("configs/small.yaml")   # from file
    cfg = PRESETS["small"]                     # built-in preset
"""

import copy
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    yaml = None


DEFAULTS = {
    # Version
    "version": "v03",

    # Perceiver (C1)
    "d_model": 768,
    "n_evidence": 17,
    "d_evidence": 32,
    "img_size": 224,
    "patch_size": 16,
    "use_backbone": False,
    "backbone_type": "dinov2_vitb14",
    "backbone_freeze": True,
    "backbone_checkpoint_path": "",

    # Memory (C2) — v0.3 spatial memory
    "d_memory": 128,
    "n_state_tokens": 32,
    "bank_capacity": 256,
    "nsa_select_k": 8,
    "nsa_heads": 4,
    "nsa_confidence_bias_strength": 2.0,
    "nsa_geometry_bias_strength": 1.0,
    "nsa_top_k_branches": 2,
    "grassmannian_strength": 0.1,
    "anchor_spatial_bias_alpha": 1.0,
    "anchor_spatial_retrieval_mode": "latent_plus_3d",
    "active_to_stable_threshold": 0.6,
    "stable_recall_threshold": -1.0,
    "stable_recall_strength": 0.25,
    "stability_prune_bonus": 1.0,
    "state_recurrence_type": "cross_attention",
    "memory_use_nsa": True,
    "enable_stable_memory": True,
    "sliding_window": 4,

    # Memory (C2) — v0.1 legacy
    "d_state": 256,
    "n_ssm_layers": 6,
    "d_bus_context": 3,

    # Permanence (C3)
    "d_slot": 128,
    "n_slots": 16,
    "n_slot_iters": 3,

    # Critic (C4)
    "d_critic": 256,
    "n_critic_heads": 4,
    "n_critic_layers": 2,
    "critic_geometric_conflict_scale": 8.0,
    "critic_geometric_clean_bias": -2.0,

    # Composer (C5) — v0.3 router
    "n_regimes": 6,
    "n_models": 8,
    "d_routing": 64,
    "cost_alpha": 0.5,

    # Training
    "batch_size": 4,
    "lr": 1e-4,
    "weight_decay": 1e-5,
    "epochs": 100,
    "warmup_epochs": 5,
    "grad_clip": 1.0,
    "amp": True,
    "gradient_checkpointing": False,

    # Loss weights
    "w_pointmap": 1.0,
    "w_critic_p1": 0.5,
    "w_critic_p5": 0.3,
    "w_memory_p2": 0.3,
    "w_memory_p3": 0.2,
    "w_permanence_p4": 0.5,
    "w_action_entropy": 0.1,
    "w_retrieval": 0.1,
    "w_retrieval_quality": 0.05,
    "w_routing": 0.05,
    "w_geometric_consistency": 0.05,
    "w_sampson_distance": 0.05,
    "w_covisibility_consistency": 0.05,
    "w_drift_consistency": 0.1,
    "w_state_drift_regularization": 0.01,
    "w_memory_consistency": 0.0,
    "w_cross_window_pointmap": 0.0,
    "w_anchor_reuse": 0.0,

    # Data
    "data_root": "/hdd3/kykt26/data",
    "dataset": "synthetic",
    "num_workers": 4,
    "n_frames_per_window": 4,
    "sequence_length": 3,
    "kitti_window_frames": 8,
    "kitti_window_overlap": 4,
    "kitti_windows_per_sample": 4,
    "kitti_min_sequence_frames": 50,
    "kitti_max_frames_per_sequence": 100,
    "kitti_max_sequences": 0,
    "tbptt_detach_every": 1,
    "train_mode": "full",
    "regime_labels_path": "/hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json",
    "oracle_labels_path": "/hdd3/kykt26/code/dream3r/runs/stage3_oracle_labels/oracle_expert_labels.json",

    # DDP
    "gpus": "0,1",
    "dist_backend": "nccl",

    # Logging
    "log_dir": "/hdd3/kykt26/code/dream3r/runs",
    "save_dir": "/hdd3/kykt26/code/dream3r/checkpoints",
    "log_every": 50,
    "save_every_epoch": 10,
    "eval_every_epoch": 5,
}


PRESETS = {
    "small": {
        **DEFAULTS,
        "use_backbone": False,
        "gpus": "0,1",
    },
    "small_v01": {
        **DEFAULTS,
        "version": "v01",
        "use_backbone": False,
        "gpus": "0,1",
    },
    "small_vit": {
        **DEFAULTS,
        "use_backbone": True,
        "gpus": "0,1",
        "batch_size": 2,
    },
    "small_real": {
        **DEFAULTS,
        "use_backbone": True,
        "backbone_type": "dinov3_vitb16_onnx",
        "backbone_checkpoint_path": "/hdd3/kykt26/checkpoints/dinov3-vitb16-onnx/onnx/model.onnx",
        "batch_size": 1,
        "gpus": "0",
    },
    "memory_only": {
        **DEFAULTS,
        "dataset": "kitti_long",
        "train_mode": "memory_only",
        "use_backbone": False,
        "batch_size": 4,
        "epochs": 20,
        "warmup_epochs": 1,
        "gpus": "0",
        "num_workers": 2,
        "save_dir": "/hdd3/kykt26/checkpoints/memory_only_v1",
        "kitti_max_sequences": 2,
        "kitti_max_frames_per_sequence": 60,
        "w_pointmap": 0.0,
        "w_critic_p1": 0.0,
        "w_critic_p5": 0.0,
        "w_memory_p2": 0.0,
        "w_memory_p3": 0.0,
        "w_permanence_p4": 0.0,
        "w_action_entropy": 0.0,
        "w_retrieval": 0.05,
        "w_retrieval_quality": 0.05,
        "w_routing": 0.0,
        "w_geometric_consistency": 0.0,
        "w_sampson_distance": 0.0,
        "w_covisibility_consistency": 0.0,
        "w_drift_consistency": 0.1,
        "w_state_drift_regularization": 0.001,
        "w_memory_consistency": 0.05,
        "w_cross_window_pointmap": 0.0,
        "w_anchor_reuse": 0.1,
    },
    "router_only": {
        **DEFAULTS,
        "dataset": "kitti_long",
        "train_mode": "router_only",
        "use_backbone": False,
        "batch_size": 16,
        "epochs": 100,
        "lr": 1e-2,
        "warmup_epochs": 1,
        "gpus": "0",
        "num_workers": 0,
        "d_routing": 32,
        "cost_alpha": 0.0,
        "save_dir": "/hdd3/kykt26/checkpoints/router_only_v1",
    },
    "base": {
        **DEFAULTS,
        "use_backbone": True,
        "d_memory": 256,
        "n_state_tokens": 64,
        "bank_capacity": 512,
        "nsa_select_k": 16,
        "nsa_heads": 8,
        "sliding_window": 8,
        "d_slot": 256,
        "n_slots": 32,
        "d_critic": 512,
        "n_critic_layers": 4,
        "d_routing": 128,
        "gpus": "0,1,2",
        "batch_size": 2,
    },
}


def load_config(path: Optional[str] = None, preset: str = "small",
                overrides: Optional[dict] = None) -> dict:
    """
    Load config with priority: overrides > yaml file > preset > defaults.
    """
    cfg = copy.deepcopy(PRESETS.get(preset, DEFAULTS))

    if path and yaml:
        p = Path(path)
        if p.exists():
            with open(p) as f:
                file_cfg = yaml.safe_load(f) or {}
            cfg.update(file_cfg)

    if overrides:
        cfg.update(overrides)

    return cfg


def save_config(cfg: dict, path: str):
    if yaml is None:
        raise ImportError("pyyaml required: pip install pyyaml")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)


def config_to_model_args(cfg: dict) -> dict:
    """Extract only the keys Dream3R.__init__ needs."""
    args = {
        "version": cfg.get("version", "v03"),
        "d_model": cfg["d_model"],
        "n_evidence": cfg["n_evidence"],
        "d_evidence": cfg["d_evidence"],
        "d_slot": cfg["d_slot"],
        "n_slots": cfg["n_slots"],
        "d_critic": cfg["d_critic"],
        "critic_geometric_conflict_scale": cfg.get("critic_geometric_conflict_scale", 8.0),
        "critic_geometric_clean_bias": cfg.get("critic_geometric_clean_bias", -2.0),
        "n_regimes": cfg["n_regimes"],
        "use_backbone": cfg["use_backbone"],
        "img_size": cfg["img_size"],
        "backbone_type": cfg.get("backbone_type", "dinov2_vitb14"),
        "backbone_freeze": cfg.get("backbone_freeze", True),
        "backbone_checkpoint_path": cfg.get("backbone_checkpoint_path", ""),
        "profile": cfg.get("profile", False),
    }
    if cfg.get("version", "v03") == "v01":
        args.update({
            "d_state": cfg["d_state"],
            "n_ssm_layers": cfg["n_ssm_layers"],
            "n_models": cfg.get("n_models", 8),
        })
    else:
        args.update({
            "d_memory": cfg.get("d_memory", 128),
            "n_state_tokens": cfg.get("n_state_tokens", 32),
            "bank_capacity": cfg.get("bank_capacity", 256),
            "nsa_select_k": cfg.get("nsa_select_k", 8),
            "nsa_heads": cfg.get("nsa_heads", 4),
            "nsa_confidence_bias_strength": cfg.get("nsa_confidence_bias_strength", 2.0),
            "nsa_geometry_bias_strength": cfg.get("nsa_geometry_bias_strength", 1.0),
            "nsa_top_k_branches": cfg.get("nsa_top_k_branches", 2),
            "grassmannian_strength": cfg.get("grassmannian_strength", 0.1),
            "anchor_spatial_bias_alpha": cfg.get("anchor_spatial_bias_alpha", 1.0),
            "anchor_spatial_retrieval_mode": cfg.get("anchor_spatial_retrieval_mode", "latent_plus_3d"),
            "active_to_stable_threshold": cfg.get("active_to_stable_threshold", 0.6),
            "stable_recall_threshold": cfg.get("stable_recall_threshold", -1.0),
            "stable_recall_strength": cfg.get("stable_recall_strength", 0.25),
            "stability_prune_bonus": cfg.get("stability_prune_bonus", 1.0),
            "state_recurrence_type": cfg.get("state_recurrence_type", "cross_attention"),
            "memory_use_nsa": cfg.get("memory_use_nsa", True),
            "enable_stable_memory": cfg.get("enable_stable_memory", True),
            "sliding_window": cfg.get("sliding_window", 4),
            "d_routing": cfg.get("d_routing", 64),
            "cost_alpha": cfg.get("cost_alpha", 0.5),
        })
    return args
