import math, random
from collections import namedtuple
from numbers import Number
import routing, services
import sims4.geometry as sgeometry
import sims4.math as smath
from _math import Quaternion as _Quaternion
MAX_FLOAT = 3.402823466e+38
MAX_UINT64 = 18446744073709551615
MAX_INT64 = 9223372036854775807
MIN_INT64 = -9223372036854775808
MAX_UINT32 = 4294967295
MAX_INT32 = 2147483647
MIN_INT32 = -2147483648
MAX_UINT24 = 16777216
MAX_INT24 = 8388607
MIN_INT24 = -8388608
MAX_UINT16 = 65535
MAX_INT16 = 32767
MIN_INT16 = -32768
MAX_UINT12 = 2048
MAX_INT12 = 1023
MIN_INT12 = -1024

class Vector3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __new__(cls, x, y, z, **kwargs):
        return (smath.Vector3)(x, y, z, **kwargs)


class Transform:
    IDENTITY = smath.Transform.IDENTITY()

    def __init__(self, translation, orientation=smath.Quaternion.IDENTITY()):
        self.translation = translation
        self.orientation = orientation

    def __new__(cls, translation, orientation=smath.Quaternion.IDENTITY()):
        return smath.Transform(translation, orientation)

    @staticmethod
    def concatenate(t1, t2):
        return smath.Transform.concatenate(t1, t2)


class Quaternion:
    IDENTITY = _Quaternion.IDENTITY()

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __new__(cls, x, y, z, w):
        return smath.Quaternion(x, y, z, w)

    @staticmethod
    def from_quaternion(quaternion):
        return Quaternion(clamp(-1.0, quaternion.x, 1.0), clamp(-1.0, quaternion.y, 1.0), clamp(-1.0, quaternion.z, 1.0), clamp(-1.0, quaternion.w, 1.0))

    @staticmethod
    def from_euler(pitch, yaw, roll):
        ps = math.sin(pitch / 2)
        pc = math.cos(pitch / 2)
        ys = math.sin(yaw / 2)
        yc = math.cos(yaw / 2)
        rs = math.sin(roll / 2)
        rc = math.cos(roll / 2)
        qx = rc * ps * yc + rs * pc * ys
        qy = rc * pc * ys + rs * ps * yc
        qz = rs * pc * yc - rc * ps * ys
        qw = rc * pc * yc + rs * ps * ys
        return Quaternion(qx, qy, qz, qw)

    @staticmethod
    def concatenate(q1, q2):
        return _Quaternion.concatenate(q1, q2)


class SurfaceIdentifier:

    def __init__(self, level, zone_id=None, surface_type=routing.SurfaceType.SURFACETYPE_WORLD):
        self.level = level
        self.zone_id = zone_id if zone_id is not None else services.current_zone_id()
        self.surface_type = surface_type

    def __new__(cls, level, zone_id=None, surface_type=routing.SurfaceType.SURFACETYPE_WORLD):
        return routing.SurfaceIdentifier(zone_id if zone_id is not None else services.current_zone_id(), level, surface_type)


LocationData = namedtuple("LocationData", ('position', 'level', 'orientation', 'routing_surface'))

class Location:

    def __init__(self, position, level, angle_or_quaternion, surface_override=None):
        self.position = position
        self.level = level
        self.orientation = convert_angle_to_orientation(angle_or_quaternion) if isinstance(angle_or_quaternion, Number) else angle_or_quaternion
        self.routing_surface = surface_override if surface_override is not None else SurfaceIdentifier(level)

    @staticmethod
    def copy(location, x=None, y=None, z=None, level=None, angle_or_quaternion=None, routing_surface=None):
        position = location.transform.translation
        return Location(Vector3(x or position.x, y or position.y, z or position.z), level or location.level, angle_or_quaternion or location.transform.orientation, routing_surface or location.routing_surface)

    @staticmethod
    def deconstruct(location):
        position = location.transform.translation
        orientation = location.transform.orientation
        return LocationData(Vector3(position.x, position.y, position.z), location.level, orientation, location.routing_surface)

    def __new__(cls, position, level, angle_or_quaternion, surface_override=None):
        return smath.Location(smath.Transform(position, convert_angle_to_orientation(angle_or_quaternion) if isinstance(angle_or_quaternion, Number) else angle_or_quaternion), surface_override if surface_override is not None else SurfaceIdentifier(level))


class Polygon:

    def __init__(self, vertices):
        self.vertices = vertices

    def __new__(cls, vertices, **kwargs):
        return (sgeometry.Polygon)(vertices, **kwargs)

    def normalize(self):
        pass

    def centroid(self):
        pass

    def radius(self):
        pass

    def area(self):
        pass

    def bounds(self):
        pass

    def contains(self, point):
        pass

    def intersect(self, polygon):
        pass

    def union(self, polygon):
        pass

    def subtract(self, polygon):
        pass

    def get_convex_hull(self):
        pass


def clamp(lower_bound, x, upper_bound):
    if x < lower_bound:
        return lower_bound
    if x > upper_bound:
        return upper_bound
    return x


def linear_curve(points_list):
    return smath.LinearCurve(points_list)


def normalize_vector(vector):
    return smath.vector_normalize(vector)


def flatten_vector(vector):
    return smath.vector_flatten(vector)


def vector_distance(vector_1, vector_2):
    return math.sqrt((vector_1 - vector_2).magnitude_squared())


def convert_vector3_to_angle(vector):
    return math.degrees(smath.vector3_angle(vector))


def convert_angle_to_vector3(angle, y_axis=0):
    return Vector3(math.cos(math.radians(angle)), y_axis, math.sin(math.radians(angle)))


def convert_orientation_to_angle(orientation):
    orientation = Quaternion.from_quaternion(orientation)
    return math.degrees(smath.yaw_quaternion_to_angle(orientation))


def convert_angle_to_orientation(angle):
    return smath.angle_to_yaw_quaternion(math.radians(angle))


def convert_quaternion_to_euler(x, y, z, w):
    pitch = math.atan2(2 * (w * x - y * z), 1 - 2 * (x ** 2 + y ** 2))
    yaw = math.asin(max(-1.0, min(2 * (w * y + z * x), 1.0)))
    roll = math.atan2(2 * (w * z - x * y), 1 - 2 * (y ** 2 + z ** 2))
    return (
     pitch, yaw, roll)


def quaternion_identity():
    return smath.Quaternion.IDENTITY()


def angle_between_vectors(position_1, position_2):
    return math.degrees(math.atan2(position_2.x - position_1.x, position_2.z - position_1.z))


def get_vector_offset_from_angle(angle, length):
    offset = smath.FORWARD_AXIS
    offset = smath.angle_to_yaw_quaternion(math.radians(angle)).transform_vector(offset)
    offset = smath.vector_normalize(offset) * length
    return offset


def random_int_of_bit_length(bit_length):
    if bit_length <= 0:
        raise ValueError("Bit length must be a positive integer.")
    return random.randint(2 ** (bit_length - 1), 2 ** bit_length - 1)


def splice_int64(high_value, low_value):
    return high_value - MIN_INT32 << 32 | low_value - MIN_INT32


def split_int64(value):
    low_value = (value & 4294967295) + MIN_INT32
    high_value = (value >> 32) + MIN_INT32
    return (
     high_value, low_value)


def splice_uint64(high_value, low_value):
    return high_value << 32 | low_value


def split_uint64(value):
    low_value = value & 4294967295
    high_value = value >> 32
    return (
     high_value, low_value)


def splice_int24(high_value, low_value):
    return high_value - MIN_INT12 << 12 | low_value - MIN_INT12


def split_int24(value):
    low_value = (value & 2047) + MIN_INT12
    high_value = (value >> 12) + MIN_INT12
    return (
     high_value, low_value)


def splice_uint24(high_value, low_value):
    return high_value << 12 | low_value


def split_uint24(value):
    low_value = value & 2047
    high_value = value >> 12
    return (
     high_value, low_value)
