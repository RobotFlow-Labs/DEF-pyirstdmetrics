# PRD Master - DEF-pyirstdmetrics

## Goal
Build an ANIMA-ready IRSTD evaluation module around PyIRSTDMetrics that provides reproducible pixel-level, target-level, and hybrid-level benchmarking APIs for Wave-8 defense modules.

## Paper Alignment
- Paper: `papers/2509.16888.pdf` (NeurIPS 2025)
- Core methods to preserve:
  - OPDC matching (Sec. 4.1)
  - hIoU = IoU_loc * IoU_seg (Sec. 4.2)
  - hierarchical error decomposition (Sec. 4.3)
  - protocol defaults including threshold=0.5 and distance=3 (Sec. 3.2, Sec. 4.1)

## Build Plan
| PRD | Title | Priority | Depends On | Status |
|---|---|---|---|---|
| PRD-01 | Foundation and Config Scaffold | P0 | None | DONE (initial scaffold) |
| PRD-02 | Core Metric Adapter Layer | P0 | PRD-01 | IN_PROGRESS |
| PRD-03 | Inference Input Pipeline | P0 | PRD-02 | NOT_STARTED |
| PRD-04 | Evaluation and Benchmark Reporting | P1 | PRD-03 | NOT_STARTED |
| PRD-05 | API and Docker Serving | P1 | PRD-03 | IN_PROGRESS |
| PRD-06 | ROS2 Integration | P1 | PRD-05 | NOT_STARTED |
| PRD-07 | Production Hardening and CI Tracking | P2 | PRD-04, PRD-05 | NOT_STARTED |

## Gate Summary (Autopilot)
| Gate | Result | Notes |
|---|---|---|
| Gate 0 - Session Recovery | PASS | Fresh scaffold state; no prior PRD execution found. |
| Gate 1 - Paper Alignment | PASS | Local PDF + reference repo + online metadata verified. |
| Gate 2 - Data Preflight | PASS_WITH_WARNINGS | External benchmark datasets not found locally; local test assets present. |
| Gate 3 - Infra Check | PASS_AFTER_SCAFFOLD | Required foundation files were missing and have now been created. |
| Gate 3.5 - PRD Generation | PASS | Full PRD and task structure generated. |

## Risks
1. External benchmark datasets for cross-dataset evaluation are not mounted in current environment.
2. Downstream module integration (for example DEF-dhif) depends on prediction export conventions.
3. ROS2 contracts are not yet fixed for evaluation-only modules.

## Definition of Done
1. CLI evaluates prediction/mask folders and emits standardized JSON.
2. API service exposes `/health`, `/ready`, `/predict`.
3. Results include full paper-aligned metric hierarchy.
4. Cross-module evaluation schema is stable and documented.
5. CI gate can run smoke evaluation against reference test_data.
