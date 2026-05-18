# ABL-memory-0 go/no-go summary

Status: pass

| Check | Passed |
| --- | --- |
| `shape:frame_tokens` | true |
| `shape:evidence_tokens` | true |
| `shape:point_tokens` | true |
| `shape:group_id` | true |
| `shape:is_dynamic` | true |
| `shape:is_corrupt` | true |
| `shape:expected_loop_id` | true |
| `shape:bus.dynamic_ratio` | true |
| `shape:bus.conflict_score` | true |
| `shape:bus.permanence_score` | true |
| `shape:bus.expected_future_use` | true |
| `shape:bus.reset_mask` | true |
| `reproducible_label:group_id` | true |
| `reproducible_label:is_dynamic` | true |
| `reproducible_label:is_corrupt` | true |
| `reproducible_label:expected_loop_id` | true |
| `reproducible_tensor:frame_tokens` | true |
| `reproducible_tensor:evidence_tokens` | true |
| `reproducible_tensor:point_tokens` | true |
| `oracle_bus_tags` | true |
| `raw_label_exclusion` | true |
| `output_serialization_plan` | true |

Interpretation:

- `pass` means the local P0 fixture/logging substrate is admissible for later ablation work.
- It does not validate Memory v0.3 retrieval, recurrence, reconstruction, training, or paper claims.
