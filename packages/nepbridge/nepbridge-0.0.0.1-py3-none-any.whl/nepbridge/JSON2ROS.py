import json
from geometry_msgs.msg import Accel, Point, Pose, Quaternion, Transform, Twist, Vector3, Wrench, Point32, ChannelFloat32
from sensor_msgs.msg import CameraInfo, JointState, Imu, Temperature, PointCloud
from std_msgs.msg import String, Float32, ColorRGBA, Bool, Int32


def create_ros_message(data, handle_missing_msg_type=False):

    if "msg_type" in data:
        msg_type = data["msg_type"]
    elif handle_missing_msg_type:
        print("No 'msg_type' found in the JSON data.")
        return None
    else:
        raise ValueError("No 'msg_type' found in the JSON data.")
    if msg_type == "geometry_msgs/Accel" or msg_type == "Accel":
        ros_message = create_accel_message(data)
    elif msg_type == "geometry_msgs/Point" or msg_type == "Point":
        ros_message = create_point_message(data)
    elif msg_type == "geometry_msgs/Pose" or msg_type == "Pose":
        ros_message = create_pose_message(data)
    elif msg_type == "geometry_msgs/Quaternion" or msg_type == "Quaternion":
        ros_message = create_quaternion_message(data)
    elif msg_type == "geometry_msgs/Transform" or msg_type == "Transform":
        ros_message = create_transform_message(data)
    elif msg_type == "geometry_msgs/Twist" or msg_type == "Twist":
        ros_message = convert_to_twist(data)
    elif msg_type == "geometry_msgs/Vector3" or msg_type == "Vector3":
        ros_message = convert_to_vector3(data)
    elif msg_type == "geometry_msgs/Wrench" or msg_type == "Wrench":
        ros_message = create_wrench_message(data)
    elif msg_type == "sensor_msgs/CameraInfo" or msg_type == "CameraInfo":
        ros_message = create_camera_info_message(data)
    elif msg_type == "sensor_msgs/JointState" or msg_type == "JointState":
        ros_message = create_joint_state_message(data)
    elif msg_type == "sensor_msgs/Imu" or msg_type == "Imu":
        ros_message = create_imu_message(data)
    elif msg_type == "sensor_msgs/Temperature" or msg_type == "Temperature":
        ros_message = create_temperature_message(data);
    elif msg_type == "sensor_msgs/PointCloud" or msg_type == "PointCloud":
        ros_message = create_point_cloud_message(data)
    else:
        raise ValueError("Unsupported message type: {}".format(msg_type))

    # Set the message fields based on the JSON data
    for field in ros_message.__slots__:
        if field in data:
            setattr(ros_message, field, data[field])

    return ros_message

def create_transform_message(data):
    ros_message = Transform()

    if "translation" in data:
        translation_data = data["translation"]
        if "x" in translation_data:
            ros_message.translation.x = translation_data["x"]
        if "y" in translation_data:
            ros_message.translation.y = translation_data["y"]
        if "z" in translation_data:
            ros_message.translation.z = translation_data["z"]

    if "rotation" in data:
        rotation_data = data["rotation"]
        if "x" in rotation_data:
            ros_message.rotation.x = rotation_data["x"]
        if "y" in rotation_data:
            ros_message.rotation.y = rotation_data["y"]
        if "z" in rotation_data:
            ros_message.rotation.z = rotation_data["z"]
        if "w" in rotation_data:
            ros_message.rotation.w = rotation_data["w"]

    return ros_message

def create_camera_info_message(data):
    ros_message = CameraInfo()

    if "header" in data:
        header_data = data["header"]
        if "frame_id" in header_data:
            ros_message.header.frame_id = header_data["frame_id"]

    if "height" in data:
        ros_message.height = data["height"]

    if "width" in data:
        ros_message.width = data["width"]

    if "distortion_model" in data:
        ros_message.distortion_model = data["distortion_model"]

    if "D" in data:
        ros_message.D = data["D"]

    if "K" in data:
        ros_message.K = data["K"]

    if "R" in data:
        ros_message.R = data["R"]

    if "P" in data:
        ros_message.P = data["P"]

    if "binning_x" in data:
        ros_message.binning_x = data["binning_x"]

    if "binning_y" in data:
        ros_message.binning_y = data["binning_y"]

    if "roi" in data:
        roi_data = data["roi"]
        if "x_offset" in roi_data:
            ros_message.roi.x_offset = roi_data["x_offset"]
        if "y_offset" in roi_data:
            ros_message.roi.y_offset = roi_data["y_offset"]
        if "height" in roi_data:
            ros_message.roi.height = roi_data["height"]
        if "width" in roi_data:
            ros_message.roi.width = roi_data["width"]
        if "do_rectify" in roi_data:
            ros_message.roi.do_rectify = roi_data["do_rectify"]

    return ros_message

def create_temperature_message(data):
    ros_message = Temperature()

    if "header" in data:
        header_data = data["header"]
        if "frame_id" in header_data:
            ros_message.header.frame_id = header_data["frame_id"]

    if "temperature" in data:
        ros_message.temperature = data["temperature"]

    if "variance" in data:
        ros_message.variance = data["variance"]

    return ros_message

def create_imu_message(data):
    ros_message = Imu()

    if "header" in data:
        header_data = data["header"]
        if "frame_id" in header_data:
            ros_message.header.frame_id = header_data["frame_id"]

    if "orientation" in data:
        orientation_data = data["orientation"]
        if "x" in orientation_data:
            ros_message.orientation.x = orientation_data["x"]
        if "y" in orientation_data:
            ros_message.orientation.y = orientation_data["y"]
        if "z" in orientation_data:
            ros_message.orientation.z = orientation_data["z"]
        if "w" in orientation_data:
            ros_message.orientation.w = orientation_data["w"]

    if "angular_velocity" in data:
        angular_velocity_data = data["angular_velocity"]
        if "x" in angular_velocity_data:
            ros_message.angular_velocity.x = angular_velocity_data["x"]
        if "y" in angular_velocity_data:
            ros_message.angular_velocity.y = angular_velocity_data["y"]
        if "z" in angular_velocity_data:
            ros_message.angular_velocity.z = angular_velocity_data["z"]

    if "linear_acceleration" in data:
        linear_acceleration_data = data["linear_acceleration"]
        if "x" in linear_acceleration_data:
            ros_message.linear_acceleration.x = linear_acceleration_data["x"]
        if "y" in linear_acceleration_data:
            ros_message.linear_acceleration.y = linear_acceleration_data["y"]
        if "z" in linear_acceleration_data:
            ros_message.linear_acceleration.z = linear_acceleration_data["z"]

    if "orientation_covariance" in data:
        ros_message.orientation_covariance = data["orientation_covariance"]

    if "angular_velocity_covariance" in data:
        ros_message.angular_velocity_covariance = data["angular_velocity_covariance"]

    if "linear_acceleration_covariance" in data:
        ros_message.linear_acceleration_covariance = data["linear_acceleration_covariance"]

    return ros_message

def create_point_cloud_message(data):
    ros_message = PointCloud()

    if "header" in data:
        header_data = data["header"]
        if "frame_id" in header_data:
            ros_message.header.frame_id = header_data["frame_id"]

    if "points" in data:
        points_data = data["points"]
        for point_data in points_data:
            point = Point32()
            if "x" in point_data:
                point.x = point_data["x"]
            if "y" in point_data:
                point.y = point_data["y"]
            if "z" in point_data:
                point.z = point_data["z"]
            ros_message.points.append(point)

    if "channels" in data:
        channels_data = data["channels"]
        for channel_data in channels_data:
            channel = ChannelFloat32()
            if "name" in channel_data:
                channel.name = channel_data["name"]
            if "values" in channel_data:
                channel.values = channel_data["values"]
            ros_message.channels.append(channel)

    return ros_message

def create_wrench_message(data):
    ros_message = Wrench()

    if "force" in data:
        force_data = data["force"]
        if "x" in force_data:
            ros_message.force.x = force_data["x"]
        if "y" in force_data:
            ros_message.force.y = force_data["y"]
        if "z" in force_data:
            ros_message.force.z = force_data["z"]

    if "torque" in data:
        torque_data = data["torque"]
        if "x" in torque_data:
            ros_message.torque.x = torque_data["x"]
        if "y" in torque_data:
            ros_message.torque.y = torque_data["y"]
        if "z" in torque_data:
            ros_message.torque.z = torque_data["z"]

    return ros_message

def create_joint_state_message(data):
    ros_message = JointState()

    if "name" in data:
        ros_message.name = data["name"]

    if "position" in data:
        ros_message.position = data["position"]

    if "velocity" in data:
        ros_message.velocity = data["velocity"]

    if "effort" in data:
        ros_message.effort = data["effort"]

    return ros_message

def convert_to_twist(data):
    twist = Twist()
    if "linear" in data:
        linear_data = data["linear"]
        if "x" in linear_data:
            twist.linear.x = linear_data["x"]
        if "y" in linear_data:
            twist.linear.y = linear_data["y"]
        if "z" in linear_data:
            twist.linear.z = linear_data["z"]
    if "angular" in data:
        angular_data = data["angular"]
        if "x" in angular_data:
            twist.angular.x = angular_data["x"]
        if "y" in angular_data:
            twist.angular.y = angular_data["y"]
        if "z" in angular_data:
            twist.angular.z = angular_data["z"]
    return twist

def convert_to_vector3(data):
    vector3 = Vector3()
    if "x" in data:
        vector3.x = data["x"]
    if "y" in data:
        vector3.y = data["y"]
    if "z" in data:
        vector3.z = data["z"]
    return vector3

def create_quaternion_message(data):
    ros_message = Quaternion()

    if "x" in data:
        ros_message.x = data["x"]
    if "y" in data:
        ros_message.y = data["y"]
    if "z" in data:
        ros_message.z = data["z"]
    if "w" in data:
        ros_message.w = data["w"]

    return ros_message

def create_pose_message(data):
    ros_message = Pose()

    if "position" in data:
        position_data = data["position"]
        if "x" in position_data:
            ros_message.position.x = position_data["x"]
        if "y" in position_data:
            ros_message.position.y = position_data["y"]
        if "z" in position_data:
            ros_message.position.z = position_data["z"]

    if "orientation" in data:
        orientation_data = data["orientation"]
        if "x" in orientation_data:
            ros_message.orientation.x = orientation_data["x"]
        if "y" in orientation_data:
            ros_message.orientation.y = orientation_data["y"]
        if "z" in orientation_data:
            ros_message.orientation.z = orientation_data["z"]
        if "w" in orientation_data:
            ros_message.orientation.w = orientation_data["w"]

    return ros_message

def create_point_message(data):
    ros_message = Point()

    if "x" in data:
        ros_message.x = data["x"]
    if "y" in data:
        ros_message.y = data["y"]
    if "z" in data:
        ros_message.z = data["z"]

    return ros_message

def create_accel_message(data):
    ros_message = Accel()

    if "linear" in data:
        linear_data = data["linear"]
        if "x" in linear_data:
            ros_message.linear.x = linear_data["x"]
        if "y" in linear_data:
            ros_message.linear.y = linear_data["y"]
        if "z" in linear_data:
            ros_message.linear.z = linear_data["z"]

    if "angular" in data:
        angular_data = data["angular"]
        if "x" in angular_data:
            ros_message.angular.x = angular_data["x"]
        if "y" in angular_data:
            ros_message.angular.y = angular_data["y"]
        if "z" in angular_data:
            ros_message.angular.z = angular_data["z"]

    return ros_message

def create_int32_message(data):
    ros_message = Int32()
    if "data" in data:
        ros_message.data = int(data["data"])
    return ros_message

def create_bool_message(data):
    ros_message = Bool()
    if "data" in data:
        ros_message.data = bool(data["data"])
    return ros_message

def create_color_rgba_message(data):
    ros_message = ColorRGBA()
    if "r" in data:
        ros_message.r = float(data["r"])
    if "g" in data:
        ros_message.g = float(data["g"])
    if "b" in data:
        ros_message.b = float(data["b"])
    if "a" in data:
        ros_message.a = float(data["a"])
    return ros_message

def create_float32_message(data):
    ros_message = Float32()
    if "data" in data:
        ros_message.data = float(data["data"])
    return ros_message

def create_string_message(data):
    ros_message = String()
    if "data" in data:
        ros_message.data = data["data"]
    return ros_message
