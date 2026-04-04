# PRD-01: Foundation and Config Scaffold

> Module: DEF-pyirstdmetrics | Priority: P0
> Depends on: None
> Status: DONE

## Objective
Create a buildable project skeleton with reproducible configuration and core package wiring.

## Context (from paper)
The paper provides a standardized evaluation toolkit and default protocol values (Sec. 3.2, Sec. 4.1, Sec. 5.1). The ANIMA module needs an explicit scaffold that preserves those defaults while exposing integration points.

## Acceptance Criteria
- [x] `pyproject.toml` exists with ANIMA package metadata and CLI entry points.
- [x] `src/`, `configs/`, `scripts/`, `tests/` directories exist.
- [x] Configs include paper-aligned defaults (`threshold=0.5`, `distance_threshold=3`, `overlap_threshold=0.5`).
- [x] `anima_module.yaml`, `Dockerfile.serve`, `docker-compose.serve.yml` exist.
- [ ] Test: `uv run pytest tests/test_config.py -v` passes.

## Files to Create
| File | Purpose | Paper Ref | Est. Lines |
|---|---|---|---|
| `pyproject.toml` | package + scripts | Sec. 5.1 protocol alignment | ~35 |
| `configs/default.toml` | default evaluation params | Sec. 3.2 / 4.1 | ~6 |
| `configs/paper.toml` | explicit paper-aligned config | Sec. 5.1 | ~6 |
| `anima_module.yaml` | ANIMA module contract | toolkit scope from abstract/introduction | ~20 |

## Dependencies
- `pyirstdmetrics>=1.0.2`
- `numpy`, `scipy`, `scikit-image`
- `fastapi`, `uvicorn`

## References
- Paper Sec. 3.2, Sec. 4.1, Sec. 5.1
- Reference implementation: `repositories/PyIRSTDMetrics/`
