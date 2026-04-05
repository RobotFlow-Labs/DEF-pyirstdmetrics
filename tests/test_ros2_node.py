from anima_pyirstdmetrics.ros2_node import ROS2_AVAILABLE


def test_ros2_import_flag() -> None:
    """Verify ROS2 availability detection works without crashing."""
    assert isinstance(ROS2_AVAILABLE, bool)


def test_create_node_without_rclpy() -> None:
    """On this server rclpy is not installed — create_node should raise RuntimeError."""
    if ROS2_AVAILABLE:
        import pytest
        pytest.skip("rclpy is available — cannot test offline mode")
    import pytest
    from anima_pyirstdmetrics.ros2_node import create_node
    with pytest.raises(RuntimeError, match="rclpy not available"):
        create_node()
