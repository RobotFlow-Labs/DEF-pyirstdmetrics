# PRD-07: Production Hardening and CI Tracking

> Module: DEF-pyirstdmetrics | Priority: P2
> Depends on: PRD-04, PRD-05
> Status: NOT_STARTED

## Objective
Harden evaluation pipeline for CI usage, schema stability, and operational diagnostics.

## Context (from paper)
The paper emphasizes standardized and fair evaluation. Production hardening ensures those guarantees remain stable under automation and cross-team usage.

## Acceptance Criteria
- [ ] Add deterministic JSON schema versioning.
- [ ] Add CI smoke evaluation against reference test_data.
- [ ] Add clear preflight checks for required assets and imports.
- [ ] Add changelog policy for metric-semantic changes.

## Files to Create
| File | Purpose | Paper Ref | Est. Lines |
|---|---|---|---|
| `.github/workflows/eval-smoke.yml` | CI smoke run | standardized benchmarking motivation | ~60 |
| `scripts/preflight.py` | gating checks | reproducibility and validity | ~30 |
| `CHANGELOG.md` updates | semantic change tracking | benchmarking stability | ~30 |

## References
- Paper motivation: standardized benchmarking and reproducible evaluation
