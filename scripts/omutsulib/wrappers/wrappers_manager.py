from weakref import WeakValueDictionary
import sims4.log
logger = sims4.log.Logger('IWNBedwettingMain')

class OmutsuInstanceSingleton(type):
    _is_persistent = False
    _persistence_key = None
    _weak_instances = WeakValueDictionary()
    _instances = {}

    def get_key(cls, inst_id, *args, **kwargs):
        return (
         inst_id, cls.__name__)

    def get_persistence_key(cls):
        raise NotImplementedError

    def __call__(cls, *args, **kwargs):
        inst_id = args[0]
        if cls._persistence_key is None:
            cls._persistence_key = cls.get_persistence_key()
        elif cls._persistence_key != cls.get_persistence_key():
            cls._persistence_key = cls.get_persistence_key()
            cls._weak_instances.clear()
            cls._instances.clear()
        key = cls.get_key(inst_id, *args, **kwargs)
        # logger.info('key {}'.format(key))
        if key is None:
            return (super(OmutsuInstanceSingleton, cls).__call__)(inst_id, *args, **kwargs)
        # logger.info('_is_persistent {}'.format(cls._is_persistent))
        if not cls._is_persistent:
            if key not in cls._weak_instances:
                instance = (super(OmutsuInstanceSingleton, cls).__call__)(inst_id, *args, **kwargs)
                cls._weak_instances[key] = instance
                # logger.info('weak_instance {}'.format(instance))
        if cls._is_persistent:
            if key not in cls._instances:
                instance = (super(OmutsuInstanceSingleton, cls).__call__)(inst_id, *args, **kwargs)
                cls._instances[key] = instance
                # logger.info('instance {}'.format(instance))
        instance = cls._weak_instances[key] if (not cls._is_persistent) else (cls._instances[key])
        instance._update(inst_id, *args, **kwargs)
        return instance


class OmutsuInstance:

    def __init__(self, inst_id):
        self._inst_id = inst_id

    def get_instance_id(self):
        return self._inst_id

    def _update(self, *args, **kwargs):
        pass
