import inspect


class EnumBase:
    @classmethod
    def get_enum_values(cls):
        return set(obj for name, obj in inspect.getmembers(cls) if not name.startswith('_') and not callable(obj))

    @classmethod
    def get_enum_values_ordered(cls):
        return list(obj for name, obj in inspect.getmembers(cls) if not name.startswith('_') and not callable(obj))