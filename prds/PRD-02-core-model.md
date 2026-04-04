# PRD-02: Core Metric Adapter Layer

> Module: DEF-pyirstdmetrics | Priority: P0
> Depends on: PRD-01
> Status: IN_PROGRESS

## Objective
Implement a unified evaluator that wraps PyIRSTDMetrics pixel, target, and hybrid metrics with a stable ANIMA-facing API.

## Context (from paper)
The paper identifies three hierarchical levels: pixel-level metrics (Sec. 3.2), target-level metrics and OPDC matching (Sec. 4.1), and hybrid-level hIoU with error decomposition (Sec. 4.2/4.3).

## Acceptance Criteria
- [x] Build adapter that computes all three levels in one call.
- [x] Preserve OPDC defaults: overlap threshold `0.5`, distance threshold `3`.
- [x] Include error decomposition keys: `seg_*` and `loc_*`.
- [ ] Test: `uv run pytest tests/test_evaluator_smoke.py -v` passes.

## Files to Create
| File | Purpose | Paper Ref | Est. Lines |
|---|---|---|---|
| `src/anima_pyirstdmetrics/evaluator.py` | orchestration wrapper | Sec. 3.2, 4.1, 4.2, 4.3 | ~220 |
| `src/anima_pyirstdmetrics/types.py` | typed config and data contracts | Sec. 5.1 protocol constraints | ~20 |
| `tests/test_evaluator_smoke.py` | core smoke checks | toolkit validation requirement | ~20 |

## Algorithm Detail
- Compute pixel-level confusion-matrix metrics.
- Compute target-level Pd/Fa with:
  - distance-only matching
  - shooting-rule matching
  - OPDC matching
- Compute hybrid-level hIoU and hierarchical error terms.

## References
- Paper Sec. 4.1 OPDC strategy
- Paper Eq. (7): `hIoU = IoU_loc * IoU_seg`
