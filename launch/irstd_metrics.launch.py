"""ROS2 launch file for IRSTD metrics evaluation node."""


def generate_launch_description():
    try:
        from launch import LaunchDescription
        from launch.actions import DeclareLaunchArgument
        from launch_ros.actions import Node
    except ImportError:
        raise RuntimeError(
            "ROS2 launch dependencies not available. "
            "Install ros-jazzy-launch-ros or run in API-only mode."
        )

    return LaunchDescription([
        DeclareLaunchArgument(
            "num_bins", default_value="10",
            description="Number of threshold bins for dynamic metrics",
        ),
        DeclareLaunchArgument(
            "threshold", default_value="0.5",
            description="Binary threshold for pixel-level metrics",
        ),
        DeclareLaunchArgument(
            "distance_threshold", default_value="3",
            description="Centroid distance threshold for target matching",
        ),
        DeclareLaunchArgument(
            "overlap_threshold", default_value="0.5",
            description="IoU overlap threshold for OPDC matching",
        ),
        Node(
            package="anima_pyirstdmetrics",
            executable="irstd_metrics_node",
            name="irstd_metrics_node",
            output="screen",
            parameters=[{
                "num_bins": 10,
                "threshold": 0.5,
                "distance_threshold": 3,
                "overlap_threshold": 0.5,
            }],
        ),
    ])
