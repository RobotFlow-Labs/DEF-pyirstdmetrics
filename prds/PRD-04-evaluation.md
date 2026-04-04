# PRD-04: Evaluation and Benchmark Reporting

> Module: DEF-pyirstdmetrics | Priority: P1
> Depends on: PRD-03
> Status: NOT_STARTED

## Objective
Add standardized result export and comparison reports for cross-module benchmarking.

## Context (from paper)
The paper emphasizes cross-dataset analysis and robust model comparison (Sec. 5.2). ANIMA requires portable JSON outputs for CI/CD and defense benchmarking dashboards.

## Acceptance Criteria
- [ ] Emit stable JSON schema with module metadata + metric hierarchy.
- [ ] Add script for comparing multiple JSON results.
- [ ] Include hIoU and detailed error decomposition in report output.
- [ ] Include provenance fields (timestamp, config, source paths).

## Files to Create
| File | Purpose | Paper Ref | Est. Lines |
|---|---|---|---|
| `src/anima_pyirstdmetrics/report.py` | JSON serialization + compare | Sec. 5.2 | ~140 |
| `benchmarks/README.md` | benchmark conventions and schema | Sec. 5.2 | ~120 |
| `scripts/export_report.py` | export utility CLI | reproducibility requirement | ~70 |

## References
- Paper Sec. 5.2 (holistic performance, cross-dataset generalization)
