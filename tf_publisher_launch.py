from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch.utilities import perform_substitutions
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):

    eye = perform_substitutions(context, [LaunchConfiguration('eye')])

    aruco_tf_params = {
        'image_is_rectified': True,
        'marker_size': LaunchConfiguration('marker_size'),
        'reference_frame': LaunchConfiguration('reference_frame'),
        'camera_frame': LaunchConfiguration('camera_frame'),
        'marker_frame': LaunchConfiguration('marker_frame'),
        'corner_refinement': LaunchConfiguration('corner_refinement'),
    }

    aruco_tf = Node(
        package='aruco_ros',
        executable='tf_publisher',
        parameters=[aruco_tf_params],
        remappings=[('/image', '/image_raw')],
    )

    return [aruco_tf]


def generate_launch_description():

    marker_size_arg = DeclareLaunchArgument(
        'marker_size', default_value='0.34',
        description='Marker size in m. '
    )

    eye_arg = DeclareLaunchArgument(
        'eye', default_value='left',
        description='Eye. ',
        choices=['left', 'right'],
    )


    marker_frame_arg = DeclareLaunchArgument(
        'marker_frame', default_value='Id',
        description='Frame in which the marker pose will be refered. '
    )

    reference_frame_arg = DeclareLaunchArgument(
        'reference_frame', default_value='map',
        description='Reference frame. '
        'Leave it empty and the pose will be published wrt param parent_name. '
    )

    camera_frame_arg = DeclareLaunchArgument(
        'camera_frame', default_value='camera',
        description='Camera frame. '
    )

    corner_refinement_arg = DeclareLaunchArgument(
        'corner_refinement', default_value='LINES',
        description='Corner Refinement. ',
        choices=['NONE', 'HARRIS', 'LINES', 'SUBPIX'],
    )


    # Create the launch description and populate
    ld = LaunchDescription()

    ld.add_action(marker_size_arg)
    ld.add_action(eye_arg)
    ld.add_action(marker_frame_arg)
    ld.add_action(reference_frame_arg)
    ld.add_action(camera_frame_arg)
    ld.add_action(corner_refinement_arg)

    
    ld.add_action(OpaqueFunction(function=launch_setup))

    return ld
