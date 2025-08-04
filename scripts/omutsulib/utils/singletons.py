from types import MappingProxyType
from omutsulib.utils.math import Vector3, Quaternion, Transform

class DefaultType:
    pass


class ResultType:

    def __init__(self, result, reason=None):
        self.result = result
        self.reason = reason

    def __bool__(self):
        return self.result

    def get_reason(self):
        return self.reason


DEFAULT = DefaultType()
DEFAULT_TRUE = ResultType(True)
DEFAULT_FALSE = ResultType(False)
EMPTY_SET = frozenset()
EMPTY_DICT = MappingProxyType({})
ZERO_VECTOR3 = Vector3(0.0, 0.0, 0.0)
ZERO_TRANSFORM = Transform(Vector3(0.0, 0.0, 0.0), Quaternion(0.0, 0.0, 0.0, 0.0))
