# PRD-05: API and Docker Serving

> Module: DEF-pyirstdmetrics | Priority: P1
> Depends on: PRD-03
> Status: IN_PROGRESS

## Objective
Ship a service interface exposing health/readiness and evaluation endpoints for integration pipelines.

## Context (from paper)
The paper releases an evaluation toolkit for standardized benchmarking. This PRD operationalizes toolkit access in a service form for ANIMA environments.

## Acceptance Criteria
- [x] FastAPI app with `/health`, `/ready`, `/predict`.
- [x] Docker service files exist and build path is defined.
- [ ] Service response schema is versioned and documented.
- [ ] Add endpoint validation tests.

## Files to Create
| File | Purpose | Paper Ref | Est. Lines |
|---|---|---|---|
| `src/anima_pyirstdmetrics/serve.py` | API endpoints | toolkit dissemination intent (abstract) | ~70 |
| `Dockerfile.serve` | container runtime | deployment for benchmarking infra | ~15 |
| `docker-compose.serve.yml` | local compose profile | service orchestration | ~12 |

## References
- Paper abstract: open-source toolkit for standardized benchmarking
