"""ROS2 evaluation node for IRSTD metrics.

Subscribes to prediction/mask image pairs, publishes evaluation results.
Falls back gracefully if rclpy is not available (API-only mode).
"""

import json
from pathlib import Path

try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String

    ROS2_AVAILABLE = True
except ImportError:
    ROS2_AVAILABLE = False

from .evaluator import evaluate_directory
from .report import build_report
from .types import EvalConfig


class IRSTDMetricsNode:
    """ROS2 node that evaluates IRSTD predictions on demand.

    Subscribes to:
        /irstd_eval/request (std_msgs/String) — JSON with pred_dir, mask_dir, dataset_name

    Publishes to:
        /irstd_eval/result (std_msgs/String) — JSON evaluation report
    """

    def __init__(self, cfg: EvalConfig | None = None):
        self.cfg = cfg or EvalConfig()
        if not ROS2_AVAILABLE:
            raise RuntimeError(
                "rclpy not available. Install ros-jazzy-rclpy or run in API-only mode."
            )
        rclpy.init()
        self._node = Node("irstd_metrics_node")
        self._pub = self._node.create_publisher(String, "/irstd_eval/result", 10)
        self._sub = self._node.create_subscription(
            String, "/irstd_eval/request", self._on_request, 10
        )
        self._node.get_logger().info("IRSTDMetricsNode ready")

    def _on_request(self, msg) -> None:
        try:
            req = json.loads(msg.data)
            pred_dir = Path(req["pred_dir"])
            mask_dir = Path(req["mask_dir"])
            dataset_name = req.get("dataset_name", "unknown")

            metrics = evaluate_directory(pred_dir, mask_dir, cfg=self.cfg)
            report = build_report(
                metrics, dataset_name=dataset_name, config=self.cfg,
                pred_dir=str(pred_dir), mask_dir=str(mask_dir),
            )

            out = String()
            out.data = json.dumps(report)
            self._pub.publish(out)
            self._node.get_logger().info(
                f"Published eval result for {dataset_name} ({metrics.get('num_pairs', 0)} pairs)"
            )
        except Exception as exc:
            self._node.get_logger().error(f"Eval request failed: {exc}")

    def spin(self) -> None:
        rclpy.spin(self._node)

    def destroy(self) -> None:
        self._node.destroy_node()
        rclpy.shutdown()


def create_node(cfg: EvalConfig | None = None) -> IRSTDMetricsNode:
    """Create and return an IRSTDMetricsNode instance."""
    return IRSTDMetricsNode(cfg=cfg)
