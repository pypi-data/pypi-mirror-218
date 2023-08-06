import json
from geometry_msgs.msg import Accel, Point, Pose, Quaternion, Transform, Twist, Vector3, Wrench, Point32
from sensor_msgs.msg import CameraInfo, JointState, Imu, Temperature, PointCloud
from std_msgs.msg import String, Float32, ColorRGBA, Bool, Int32


def create_json_message_from_transform(ros_message):
    json_message = {
        "translation": {
            "x": ros_message.translation.x,
            "y": ros_message.translation.y,
            "z": ros_message.translation.z
        },
        "rotation": {
            "x": ros_message.rotation.x,
            "y": ros_message.rotation.y,
            "z": ros_message.rotation.z,
            "w": ros_message.rotation.w
        },
        "msg_type": "geometry_msgs/Transform"
    }
    return json_message

def create_json_message_from_twist(ros_message):
    json_message = {
        "linear": {
            "x": ros_message.linear.x,
            "y": ros_message.linear.y,
            "z": ros_message.linear.z
        },
        "angular": {
            "x": ros_message.angular.x,
            "y": ros_message.angular.y,
            "z": ros_message.angular.z
        },
        "msg_type": "geometry_msgs/Twist"
    }
    return json_message

def create_json_message_from_vector3(ros_message):
    json_message = {
        "x": ros_message.x,
        "y": ros_message.y,
        "z": ros_message.z,
        "msg_type": "geometry_msgs/Vector3"
    }
    return json_message

def create_json_message_from_wrench(ros_message):
    json_message = {
        "force": {
            "x": ros_message.force.x,
            "y": ros_message.force.y,
            "z": ros_message.force.z
        },
        "torque": {
            "x": ros_message.torque.x,
            "y": ros_message.torque.y,
            "z": ros_message.torque.z
        },
        "msg_type": "geometry_msgs/Wrench"
    }
    return json_message


def create_json_message_from_accel(ros_message):
    json_message = {
        "linear": {
            "x": ros_message.linear.x,
            "y": ros_message.linear.y,
            "z": ros_message.linear.z
        },
        "angular": {
            "x": ros_message.angular.x,
            "y": ros_message.angular.y,
            "z": ros_message.angular.z
        },
        "msg_type": "geometry_msgs/Accel"
    }
    return json_message

def create_json_message_from_point(ros_message):
    json_message = {
        "x": ros_message.x,
        "y": ros_message.y,
        "z": ros_message.z,
        "msg_type": "geometry_msgs/Point"
    }
    return json_message

def create_json_message_from_pose(ros_message):
    json_message = {
        "position": {
            "x": ros_message.position.x,
            "y": ros_message.position.y,
            "z": ros_message.position.z
        },
        "orientation": {
            "x": ros_message.orientation.x,
            "y": ros_message.orientation.y,
            "z": ros_message.orientation.z,
            "w": ros_message.orientation.w
        },
        "msg_type": "geometry_msgs/Pose"
    }
    return json_message

def create_json_message_from_quaternion(ros_message):
    json_message = {
        "x": ros_message.x,
        "y": ros_message.y,
        "z": ros_message.z,
        "w": ros_message.w,
        "msg_type": "geometry_msgs/Quaternion"
    }
    return json_message


def create_json_message_from_int32(ros_message):
    json_message = {
        "data": ros_message.data,
        "msg_type": "std_msgs/Int32"
    }
    return json_message

def create_json_message_from_string(ros_message):
    json_message = {
        "data": ros_message.data,
        "msg_type": "std_msgs/String"
    }
    return json_message

def create_json_message_from_float32(ros_message):
    json_message = {
        "data": ros_message.data,
        "msg_type": "std_msgs/Float32"
    }
    return json_message

def create_json_message_from_colorrgba(ros_message):
    json_message = {
        "r": ros_message.r,
        "g": ros_message.g,
        "b": ros_message.b,
        "a": ros_message.a,
        "msg_type": "std_msgs/ColorRGBA"
    }
    return json_message

def create_json_message_from_bool(ros_message):
    json_message = {
        "data": ros_message.data,
        "msg_type": "std_msgs/Bool"
    }
    return json_message

def create_json_message_from_camerainfo(ros_message):
    json_message = {
        "header": {
            "seq": ros_message.header.seq,
            "stamp": {
                "secs": ros_message.header.stamp.secs,
                "nsecs": ros_message.header.stamp.nsecs
            },
            "frame_id": ros_message.header.frame_id
        },
        "height": ros_message.height,
        "width": ros_message.width,
        "distortion_model": ros_message.distortion_model,
        "D": ros_message.D,
        "K": ros_message.K,
        "R": ros_message.R,
        "P": ros_message.P,
        "binning_x": ros_message.binning_x,
        "binning_y": ros_message.binning_y,
        "roi": {
            "x_offset": ros_message.roi.x_offset,
            "y_offset": ros_message.roi.y_offset,
            "height": ros_message.roi.height,
            "width": ros_message.roi.width,
            "do_rectify": ros_message.roi.do_rectify
        },
        "msg_type": "sensor_msgs/CameraInfo"
    }
    return json_message

def create_json_message_from_jointstate(ros_message):
    json_message = {
        "header": {
            "seq": ros_message.header.seq,
            "stamp": {
                "secs": ros_message.header.stamp.secs,
                "nsecs": ros_message.header.stamp.nsecs
            },
            "frame_id": ros_message.header.frame_id
        },
        "name": ros_message.name,
        "position": ros_message.position,
        "velocity": ros_message.velocity,
        "effort": ros_message.effort,
        "msg_type": "sensor_msgs/JointState"
    }
    return json_message

def create_json_message_from_imu(ros_message):
    json_message = {
        "header": {
            "seq": ros_message.header.seq,
            "stamp": {
                "secs": ros_message.header.stamp.secs,
                "nsecs": ros_message.header.stamp.nsecs
            },
            "frame_id": ros_message.header.frame_id
        },
        "orientation": {
            "x": ros_message.orientation.x,
            "y": ros_message.orientation.y,
            "z": ros_message.orientation.z,
            "w": ros_message.orientation.w
        },
        "orientation_covariance": ros_message.orientation_covariance,
        "angular_velocity": {
            "x": ros_message.angular_velocity.x,
            "y": ros_message.angular_velocity.y,
            "z": ros_message.angular_velocity.z
        },
        "angular_velocity_covariance": ros_message.angular_velocity_covariance,
        "linear_acceleration": {
            "x": ros_message.linear_acceleration.x,
            "y": ros_message.linear_acceleration.y,
            "z": ros_message.linear_acceleration.z
        },
        "linear_acceleration_covariance": ros_message.linear_acceleration_covariance,
        "msg_type": "sensor_msgs/Imu"
    }
    return json_message

def create_json_message_from_temperature(ros_message):
    json_message = {
        "header": {
            "seq": ros_message.header.seq,
            "stamp": {
                "secs": ros_message.header.stamp.secs,
                "nsecs": ros_message.header.stamp.nsecs
            },
            "frame_id": ros_message.header.frame_id
        },
        "temperature": ros_message.temperature,
        "variance": ros_message.variance,
        "msg_type": "sensor_msgs/Temperature"
    }
    return json_message
def create_json_message_from_pointcloud(ros_message):
    points = []
    for point in ros_message.points:
        points.append({
            "x": point.x,
            "y": point.y,
            "z": point.z
        })

    json_message = {
        "header": {
            "seq": ros_message.header.seq,
            "stamp": {
                "secs": ros_message.header.stamp.secs,
                "nsecs": ros_message.header.stamp.nsecs
            },
            "frame_id": ros_message.header.frame_id
        },
        "points": points,
        "channels": ros_message.channels,
        "msg_type": "sensor_msgs/PointCloud"
    }
    return json_message
