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
| PRD-01 | Foundation and Config Scaffold | P0 | None | DONE |
| PRD-02 | Core Metric Adapter Layer | P0 | PRD-01 | DONE |
| PRD-03 | Inference Input Pipeline | P0 | PRD-02 | DONE |
| PRD-04 | Evaluation and Benchmark Reporting | P1 | PRD-03 | DONE |
| PRD-05 | API and Docker Serving | P1 | PRD-03 | DONE |
| PRD-06 | ROS2 Integration | P1 | PRD-05 | DONE |
| PRD-07 | Production Hardening and CI Tracking | P2 | PRD-04, PRD-05 | DONE |

## Gate Summary (Autopilot)
| Gate | Result | Notes |
|---|---|---|
| Gate 0 - Session Recovery | PASS | Resumed from Mac scaffold on GPU server. |
| Gate 1 - Paper Alignment | PASS | Local PDF + reference repo verified. |
| Gate 2 - Data Preflight | PASS | NUAA-SIRST (427 pairs) on server. |
| Gate 3 - Infra Check | PASS | All foundation files present. |
| Gate 3.5 - PRD Generation | PASS (prev) | Full PRD and task structure from prev session. |
| Gate 4.5 - Code Review | PASS | 29 tests, all passing. |

## Test Summary
- 29 tests passing across 6 test files
- Preflight checks: all green
- NUAA-SIRST benchmark: 427 pairs evaluated successfully

## Definition of Done
1. [x] CLI evaluates prediction/mask folders and emits standardized JSON.
2. [x] API service exposes `/health`, `/ready`, `/predict`, `/info`.
3. [x] Results include full paper-aligned metric hierarchy.
4. [x] Cross-module evaluation schema is stable and documented.
5. [x] CI gate can run smoke evaluation against reference test_data.
