import sys

with open(sys.argv[1], "r") as f:
    content = f.read()

# 1. Update Perceiver __init__ to support backbone_type
old_init = '''    def __init__(self, d_model: int = 768, n_evidence: int = 17,
                 d_evidence: int = 32, img_size: int = 224,
                 patch_size: int = 16, use_backbone: bool = True):
        super().__init__()
        self.d_model = d_model
        self.n_evidence = n_evidence
        self.d_evidence = d_evidence
        self.use_backbone = use_backbone

        if use_backbone:
            try:
                import timm
                self.backbone = timm.create_model(
                    "vit_base_patch16_224", pretrained=False,
                    num_classes=0, global_pool="",
                )
                backbone_dim = 768
            except ImportError:
                self.backbone = None
                backbone_dim = d_model
            self.backbone_proj = nn.Linear(backbone_dim, d_model) if backbone_dim != d_model else nn.Identity()
        else:
            self.backbone = None
            self.backbone_proj = nn.Identity()'''

new_init = '''    def __init__(self, d_model: int = 768, n_evidence: int = 17,
                 d_evidence: int = 32, img_size: int = 224,
                 patch_size: int = 16, use_backbone: bool = True,
                 backbone_type: str = "vit_base"):
        super().__init__()
        self.d_model = d_model
        self.n_evidence = n_evidence
        self.d_evidence = d_evidence
        self.use_backbone = use_backbone
        self.backbone_type = backbone_type

        if use_backbone:
            try:
                import timm
                BACKBONE_CONFIGS = {
                    "vit_base": ("vit_base_patch16_224", 768, {}),
                    "dinov2_s": ("vit_small_patch14_dinov2", 384, {"img_size": img_size}),
                    "dinov2_b": ("vit_base_patch14_dinov2", 768, {"img_size": img_size}),
                }
                model_name, backbone_dim, extra_kwargs = BACKBONE_CONFIGS.get(
                    backbone_type, BACKBONE_CONFIGS["vit_base"]
                )
                self.backbone = timm.create_model(
                    model_name, pretrained=False,
                    num_classes=0, global_pool="", **extra_kwargs,
                )
                if backbone_type.startswith("dinov2"):
                    for p in self.backbone.parameters():
                        p.requires_grad = False
            except ImportError:
                self.backbone = None
                backbone_dim = d_model
            self.backbone_proj = nn.Linear(backbone_dim, d_model) if backbone_dim != d_model else nn.Identity()
        else:
            self.backbone = None
            self.backbone_proj = nn.Identity()'''

assert old_init in content, "C1 old_init not found"
content = content.replace(old_init, new_init)
print("C1 backbone_type: OK")

# 2. Update MemorySSM __init__
old_mem = """    def __init__(self, d_percept: int = 768, d_evidence_flat: int = 544,
                 d_state: int = 256, n_layers: int = 6,
                 d_bus_context: int = 3):
        super().__init__()
        self.d_state = d_state
        # d_bus_context: dynamic_ratio(1) + conflict_score(1) + drift(1)
        d_input = d_percept + d_evidence_flat + d_bus_context
        self.input_proj = nn.Linear(d_input, d_state)
        self.layers = nn.ModuleList([
            nn.GRUCell(d_state, d_state) for _ in range(n_layers)
        ])
        self.norm = nn.LayerNorm(d_state)

        # A1 heads
        self.update_classifier = nn.Linear(d_state, 5)
        self.full_gate = nn.Linear(d_state, 1)
        self.pose_gate = nn.Linear(d_state, 1)
        self.kalman_gain = nn.Linear(d_state, d_state)

        # A2 write head
        self.write_head = nn.Linear(d_state, 4)
        # A3 anchor scorer
        self.anchor_scorer = nn.Linear(d_state, 1)
        # Drift proxy
        self.drift_proj = nn.Linear(d_state, 1)"""

new_mem = """    def __init__(self, d_percept: int = 768, d_evidence_flat: int = 544,
                 d_state: int = 256, n_layers: int = 6,
                 d_bus_context: int = 3, anchor_capacity: int = 256,
                 nsa_topk: int = 8, nsa_compressed: int = 32,
                 nsa_sliding_window: int = 4):
        super().__init__()
        self.d_state = d_state
        d_input = d_percept + d_evidence_flat + d_bus_context
        self.input_proj = nn.Linear(d_input, d_state)
        self.layers = nn.ModuleList([
            nn.GRUCell(d_state, d_state) for _ in range(n_layers)
        ])
        self.norm = nn.LayerNorm(d_state)

        # A1 heads
        self.update_classifier = nn.Linear(d_state, 5)
        self.full_gate = nn.Linear(d_state, 1)
        self.pose_gate = nn.Linear(d_state, 1)
        self.kalman_gain = nn.Linear(d_state, d_state)

        # A2 write head
        self.write_head = nn.Linear(d_state, 4)
        # A3 anchor scorer
        self.anchor_scorer = nn.Linear(d_state, 1)
        # Drift proxy
        self.drift_proj = nn.Linear(d_state, 1)

        # v0.2: AnchorBank + NSA
        from dream3r.memory_anchor_bank import AnchorBank
        from dream3r.nsa_attention import NSAThreeBranch
        self.anchor_bank = AnchorBank(capacity=anchor_capacity, d_anchor=d_state)
        self.nsa = NSAThreeBranch(
            d_model=d_state, n_compressed=nsa_compressed,
            topk=nsa_topk, sliding_window=nsa_sliding_window,
        )
        self.retrieval_proj = nn.Linear(d_state * 2, d_state)"""

assert old_mem in content, "C2 old_mem not found"
content = content.replace(old_mem, new_mem)
print("C2 AnchorBank+NSA init: OK")

# 3. Add sliding_buffer param
old_fwd = """                bus_conflict_score: Optional[torch.Tensor] = None,
                ) -> Dict[str, torch.Tensor]:"""

new_fwd = """                bus_conflict_score: Optional[torch.Tensor] = None,
                sliding_buffer: Optional[torch.Tensor] = None,
                ) -> Dict[str, torch.Tensor]:"""

assert old_fwd in content, "C2 old_fwd not found"
content = content.replace(old_fwd, new_fwd)
print("C2 forward signature: OK")

# 4. Add NSA retrieval before A1 classifier
old_a1 = "        # --- A1: classify then branch ---\n        update_logits = self.update_classifier(h)  # [B, 5]"

new_a1 = """        # v0.2: NSA retrieval from anchor bank
        if self.anchor_bank.occupancy > 0:
            nsa_out = self.nsa(
                h, self.anchor_bank.embeddings[:self.anchor_bank.occupancy],
                sliding_buffer=sliding_buffer,
                critic_confidence=bus_conflict_score.squeeze(-1) if bus_conflict_score is not None else None,
            )
            h = self.retrieval_proj(torch.cat([h, nsa_out["memory_output"]], dim=-1))
            h = self.norm(h)

        # --- A1: classify then branch ---
        update_logits = self.update_classifier(h)  # [B, 5]"""

assert old_a1 in content, "C2 old_a1 not found"
content = content.replace(old_a1, new_a1)
print("C2 NSA retrieval: OK")

# 5. Add anchor bank insert + occupancy to return
old_ret = '''        return {
            "latent_state": new_state,
            "update_kind": update_logits,
            "update_probs": update_probs,
            "write_decision": write_logits,
            "anchor_scores": anchor_scores,
            "latent_drift_proxy": drift,
        }'''

new_ret = '''        # v0.2: store state in anchor bank
        with torch.no_grad():
            for b in range(B):
                self.anchor_bank.insert(new_state[b].detach())

        return {
            "latent_state": new_state,
            "update_kind": update_logits,
            "update_probs": update_probs,
            "write_decision": write_logits,
            "anchor_scores": anchor_scores,
            "latent_drift_proxy": drift,
            "anchor_bank_occupancy": self.anchor_bank.occupancy,
        }'''

assert old_ret in content, "C2 old_ret not found"
content = content.replace(old_ret, new_ret, 1)
print("C2 anchor insert + return: OK")

with open(sys.argv[1], "w") as f:
    f.write(content)

print("ALL PATCHES APPLIED SUCCESSFULLY")
