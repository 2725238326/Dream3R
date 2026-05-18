# Model inventory seed

Status: seed list from Dream documents and prior survey notes. Needs source
verification and completion before being treated as the final review inventory.

## Pointmap and matching line

- DUSt3R: pointmap-based geometric 3D vision; foundation of the recent 3R line.
- MASt3R: dense matching and descriptor grounding on top of DUSt3R-style 3D.
- MASt3R-SfM: SfM-oriented refinement and reconstruction pipeline around MASt3R.
- MapAnything: broader feed-forward mapping reference; needs original-paper verification before detailed claims.

## Multi-view scaling and unified geometry

- Fast3R: many-image reconstruction in a single forward pass; useful for scale and throughput comparisons.
- MV-DUSt3R+: pose-free multi-view reconstruction path; relevant for sparse-view demos.
- VGGT: unified feed-forward geometry prediction; important reference for camera, depth, pointmap, and tracks.
- DUSt3R-MASt3R-VGGT MVS evaluation: useful for positioning accuracy and benchmark claims; must be read directly before citing.
- Pow3R: reconstruction with optional camera, pose, depth, or scene priors.
- Align3R: aligned monocular depth for dynamic videos; bridges depth estimation and DUSt3R-style alignment.

## Streaming, memory, and long-context 3R

- CUT3R: persistent state-token recurrence for continuous 3D perception.
- Spann3R: spatial memory for 3D reconstruction.
- Point3R: explicit spatial pointer memory.
- STream3R: causal streaming 3R and session-style sequential inference.
- LONG3R: long-sequence streaming memory and pruning.
- LoGeR: long-context hybrid memory, currently needs source verification.
- Mem3R: hybrid memory and test-time training direction, currently needs source verification.
- PAS3R, FILT3R, LongStream, OVGGT: memory/cache/filtering comparators recorded in Dream as later research background.
- tttLRM: test-time layer / adaptation reference for scene-specific geometry; verify whether it belongs in memory, critic, or adaptation section after reading the paper.

## Dynamic and 4D reconstruction

- MonST3R: dynamic scene geometry and motion-aware 3R.
- POMATO: dynamic-aware token routing direction.
- D^2USt3R: 4D pointmap-style extension.
- Easi3R: training-free dynamic adaptation direction.
- RayMap3R: ray-based dynamic streaming comparator.
- SLAM3R: sliding-window dense SLAM comparator.

## Test-time verification and adaptation

- Test3R: test-time geometric consistency and verification.
- TTT3R: test-time update / adaptation around CUT3R-style setup.
- G-CUT3R: guided CUT3R comparator.
- CTRL and SEAL: non-3R self-correction / adaptation analogies, to be used only if clearly marked as analogies.

## Pose-free Gaussian and visual output line

- Splatt3R: pose-free Gaussian visual output path; strong demo relevance but license/use constraints need care.
- InstantSplat: pose-free or sparse-view Gaussian output path with more engineering dependencies.
- NoPoSplat: pose-free 3DGS-related method with open-license relevance.
- 3D Gaussian Splatting and 4DGS variants: output representation and rendering side, not the same problem as 3R reconstruction.

## Supporting priors

- DINOv2 / DINOv3: visual feature priors.
- Depth Anything V2, Depth Pro, Metric3D v2: depth priors.
- CoTracker, SpatialTracker: tracking priors.
- SAM2: mask and segmentation prior.
- ActiveNeRF, FisherRF, ActiveSplat, ActiveGS: active perception and active 3DGS references; likely background rather than main 3R lineage.
- DEVO, EAG3R, Event-3DGS: event/cross-modal references; include only if the survey expands to sensor extensions.

## Immediate verification needs

- Confirm official title, authors, year, venue, and PDF URL for every core entry.
- Mark whether a method has code, checkpoints, demo, and license constraints.
- Separate methods that have been locally run from methods only recorded in research notes.
- Treat CTRL, MoE routing, Mamba, Slot Attention, and active-perception papers as analogies unless the section explicitly discusses cross-domain mechanisms.
