# PRD-06: ROS2 Integration

> Module: DEF-pyirstdmetrics | Priority: P1
> Depends on: PRD-05
> Status: NOT_STARTED

## Objective
Provide ROS2-compatible adapter so modules can stream evaluation requests/results in robotics pipelines.

## Context (from paper)
While the paper focuses on benchmarking methodology, ANIMA deployment requires ROS2 interoperability for runtime system integration.

## Acceptance Criteria
- [x] Placeholder ROS2 node module exists.
- [ ] Define message contracts for evaluation request/result payloads.
- [ ] Add launch file and minimal runtime wiring with optional dependency on `rclpy`.
- [ ] Document offline mode for non-ROS environments.

## Files to Create
| File | Purpose | Paper Ref | Est. Lines |
|---|---|---|---|
| `src/anima_pyirstdmetrics/ros2_node.py` | ROS2 adapter node | ANIMA deployment requirement | ~40 |
| `configs/ros2.toml` | ROS2 runtime settings | ANIMA integration | ~30 |
| `scripts/ros2_smoke.py` | smoke helper | deployment verification | ~40 |

## References
- ANIMA deployment conventions (module-level integration)
