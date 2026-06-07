"""
Dream3R v0.3: Control-Graph Architecture for 3D Reconstruction

Modules:
  C1 Perceiver      — ViT backbone + 17 evidence projectors
  C2 SpatialMemory  — NSA 3-branch attention + AnchorBank + state recurrence
  C3 Permanence     — Slot Attention object tracking
  C4 Critic         — Transformer verification over evidence tokens
  C5 ComposerRouter — Cost-normalized expert routing with 7 adapters
  C6 MemoryBus      — Typed tensor namespace with CR-1..CR-6 gates
"""

from dream3r.bus import MemoryBus
from dream3r.model import Dream3R, build_dream3r
from dream3r.modules import (
    Perceiver, Permanence, Critic,
    SpatialMemory, ComposerRouter,
    StateTokenRecurrence, MambaHybridRecurrence,
    MemorySSM_v01, Composer_v01,
)
from dream3r.anchor_bank import AnchorBank
from dream3r.nsa_attention import NSAAttention
from dream3r.losses import Dream3RLoss
from dream3r.gaussian_head import GaussianHead
from dream3r.release_candidate import (
    Dream3RReleaseCandidate,
    Dream3RReleaseConfig,
    build_dream3r_release_candidate,
)
from dream3r.release_v11 import (
    Dream3RDomainConditionalConfig,
    Dream3RDomainConditionalRelease,
    build_dream3r_v11_release,
)
from dream3r.proposal_free_3r_decoder import ProposalFree3RDecoder
from dream3r.foundation3r_decoder import Foundation3RDecoder, Foundation3RVGGTFeatureDecoder

__version__ = "0.3.0"
