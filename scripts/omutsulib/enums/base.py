import inspect


class EnumBase:
    @classmethod
    def get_enum_values(cls):
        return frozenset(obj for name, obj in inspect.getmembers(cls) if not name.startswith('_') and not callable(obj))

    @classmethod
    def get_enum_values_ordered(cls):
        return tuple(obj for name, obj in inspect.getmembers(cls) if not name.startswith('_') and not callable(obj))
