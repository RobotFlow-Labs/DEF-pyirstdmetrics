# PRD-03: Input and Pairing Pipeline

> Module: DEF-pyirstdmetrics | Priority: P0
> Depends on: PRD-02
> Status: NOT_STARTED

## Objective
Create robust loading/pairing pipeline for prediction and mask artifacts from external modules.

## Context (from paper)
The paper evaluates methods over dataset-wide paired predictions and GT masks (Sec. 5.1/5.2). For ANIMA, this pairing must be deterministic and module-agnostic.

## Acceptance Criteria
- [x] Pair discovery from `*-pred.png` and `*-mask.png`.
- [x] Normalization and boolean mask conversion are deterministic.
- [x] Directory evaluation returns aggregate metrics and pair count.
- [ ] CLI supports evaluating directories via config.

## Files to Create
| File | Purpose | Paper Ref | Est. Lines |
|---|---|---|---|
| `src/anima_pyirstdmetrics/dataset.py` | pairing logic | Sec. 5.1 dataset evaluation protocol | ~30 |
| `src/anima_pyirstdmetrics/cli.py` | evaluation CLI | reproducible benchmarking need in Sec. 5.2 | ~35 |
| `tests/test_dataset_pairs.py` | pairing tests | data protocol correctness | ~25 |

## References
- Paper Sec. 5.1 datasets and protocol
