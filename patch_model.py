import sys

with open(sys.argv[1], "r") as f:
    content = f.read()

# 1. Add backbone_type to Perceiver init call
old_perc = '''        self.perceiver = Perceiver(
            d_model=d_model, n_evidence=n_evidence, d_evidence=d_evidence,
            img_size=img_size, use_backbone=use_backbone,
        )'''

new_perc = '''        backbone_type = c.get("backbone_type", "vit_base")

        self.perceiver = Perceiver(
            d_model=d_model, n_evidence=n_evidence, d_evidence=d_evidence,
            img_size=img_size, use_backbone=use_backbone,
            backbone_type=backbone_type,
        )'''

assert old_perc in content, "old_perc not found"
content = content.replace(old_perc, new_perc)
print("1. backbone_type forwarded to Perceiver: OK")

# 2. Update Composer to use expert registry + add regime classifier
old_composer = '''        self.composer = Composer(n_regimes=n_regimes, n_models=n_models)'''

new_composer = '''        n_experts = c.get("n_experts", 7)
        self.composer = Composer(n_regimes=n_regimes, n_models=n_experts)

        # v0.2: regime classifier (derives regime_probs from perception)
        self.regime_classifier = nn.Linear(d_model, n_regimes)'''

assert old_composer in content, "old_composer not found"
content = content.replace(old_composer, new_composer)
print("2. Composer n_experts + regime_classifier: OK")

# 3. Update Step 5 Composer to auto-derive regime_probs if not given
old_step5 = '''        # ========== Step 5: Composer ==========
        if regime_probs is None:
            regime_probs = torch.ones(B, self.composer.n_regimes, device=device)
            regime_probs = regime_probs / self.composer.n_regimes

        comp_out = self.composer(regime_probs)'''

new_step5 = '''        # ========== Step 5: Composer ==========
        if regime_probs is None:
            regime_probs = torch.softmax(self.regime_classifier(perc_summary), dim=-1)

        comp_out = self.composer(regime_probs)'''

assert old_step5 in content, "old_step5 not found"
content = content.replace(old_step5, new_step5)
print("3. regime auto-classification from perception: OK")

# 4. Add anchor_bank_occupancy to output dict
old_return_end = '''            "contract_log": self.bus.get_contract_log(),
        }'''

new_return_end = '''            "contract_log": self.bus.get_contract_log(),
            "anchor_bank_occupancy": mem_out.get("anchor_bank_occupancy", 0),
        }'''

assert old_return_end in content, "old_return_end not found"
content = content.replace(old_return_end, new_return_end)
print("4. anchor_bank_occupancy in output: OK")

# 5. Add dinov2_s preset config
old_configs = '''CONFIGS = {
    "small": {
        "d_model": 768, "n_evidence": 17, "d_evidence": 32,
        "d_state": 256, "n_ssm_layers": 6,
        "d_slot": 128, "n_slots": 16,
        "d_critic": 256, "n_regimes": 5, "n_models": 8,
        "use_backbone": False, "img_size": 224,
    },
    "small_vit": {
        "d_model": 768, "n_evidence": 17, "d_evidence": 32,
        "d_state": 256, "n_ssm_layers": 6,
        "d_slot": 128, "n_slots": 16,
        "d_critic": 256, "n_regimes": 5, "n_models": 8,
        "use_backbone": True, "img_size": 224,
    },
}'''

new_configs = '''CONFIGS = {
    "small": {
        "d_model": 768, "n_evidence": 17, "d_evidence": 32,
        "d_state": 256, "n_ssm_layers": 6,
        "d_slot": 128, "n_slots": 16,
        "d_critic": 256, "n_regimes": 5, "n_experts": 7,
        "use_backbone": False, "img_size": 224,
    },
    "small_vit": {
        "d_model": 768, "n_evidence": 17, "d_evidence": 32,
        "d_state": 256, "n_ssm_layers": 6,
        "d_slot": 128, "n_slots": 16,
        "d_critic": 256, "n_regimes": 5, "n_experts": 7,
        "use_backbone": True, "img_size": 224,
    },
    "dinov2_s": {
        "d_model": 768, "n_evidence": 17, "d_evidence": 32,
        "d_state": 256, "n_ssm_layers": 6,
        "d_slot": 128, "n_slots": 16,
        "d_critic": 256, "n_regimes": 5, "n_experts": 7,
        "use_backbone": True, "backbone_type": "dinov2_s", "img_size": 224,
    },
}'''

assert old_configs in content, "old_configs not found"
content = content.replace(old_configs, new_configs)
print("5. dinov2_s preset + n_experts in configs: OK")

with open(sys.argv[1], "w") as f:
    f.write(content)

print("ALL MODEL.PY PATCHES APPLIED")
