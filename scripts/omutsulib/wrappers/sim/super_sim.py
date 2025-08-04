import inspect, weakref
from functools import wraps
import services
from objects import ALL_HIDDEN_REASONS_EXCEPT_UNINITIALIZED
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from omutsulib.services.persistence_service import get_persistence_service
from omutsulib.wrappers.wrappers_manager import OmutsuInstance, OmutsuInstanceSingleton
_super_sim_persistence_key_cache = None


def _update_persistence_key(from_load=False, **_):
    global _super_sim_persistence_key_cache
    if from_load:
        _super_sim_persistence_key_cache = OmutsuSimSingleton.create_persistence_key()


get_persistence_service().register_save_slot_id_update_callback(_update_persistence_key)


class OmutsuSimSingleton(OmutsuInstanceSingleton):
    _is_persistent = True

    def get_key(cls, inst_id, *args, sim_id=0, exclusive_base_wrapper=False, **kwargs):
        if exclusive_base_wrapper:
            if inst_id.__class__ is SimInfoBaseWrapper:
                return None
        _sim_id = sim_id or _get_sim_instance_id(inst_id)
        if _sim_id is not None:
            return (_sim_id, cls.__name__)
        return None

    @staticmethod
    def create_persistence_key():
        return (
         get_persistence_service().get_save_slot_guid(), get_persistence_service().get_save_slot_id())

    def get_persistence_key(cls):
        global _super_sim_persistence_key_cache
        if _super_sim_persistence_key_cache is None:
            _super_sim_persistence_key_cache = cls.create_persistence_key()
        return _super_sim_persistence_key_cache


def sim_info_required(default=None, base_wrapper=False):

    def _sim_info_required(fn):
        is_generator = inspect.isgeneratorfunction(fn)
        if not is_generator:

            @wraps(fn)
            def _sim_info_required_wrapper(self, *args, **kwargs):
                if base_wrapper:
                    if self.get_sim_info_base() is not None:
                        return fn(self, *args, **kwargs)
                if self.get_sim_info() is not None:
                    return fn(self, *args, **kwargs)
                return default

        else:

            @wraps(fn)
            def _sim_info_required_wrapper(self, *args, **kwargs):
                if base_wrapper:
                    if self.get_sim_info_base() is not None:
                        yield from fn(self, *args, **kwargs)
                if self.get_sim_info() is not None:
                    yield from fn(self, *args, **kwargs)
                else:
                    yield None

        return _sim_info_required_wrapper

    return _sim_info_required


class _SuperOmutsuSim(OmutsuInstance):

    def __init__(self, *args, sim_id=0, exclusive_base_wrapper=False):
        sim_identifier = args[0]
        self._sim_id = sim_id or _get_sim_instance_id(sim_identifier)
        self._sim_instance = weakref.ref(sim_identifier) if sim_identifier.__class__ is Sim else None
        self._sim_info_base = weakref.ref(sim_identifier) if exclusive_base_wrapper and (sim_identifier.__class__ is SimInfoBaseWrapper) else None
        self._sim_info = weakref.ref(sim_identifier) if sim_identifier.__class__ is SimInfo else None
        if self._sim_id and self._sim_info is None:
            if sim_identifier.__class__ is Sim:
                self._sim_info = weakref.ref(sim_identifier.sim_info)
        super().__init__(self._sim_id)
        self._temp_values = {}

    def __new__(cls, *args, sim_id=0, exclusive_base_wrapper=False):
        sim_identifier = args[0]
        if isinstance(sim_identifier, _SuperOmutsuSim):
            return sim_identifier
        if _get_sim_instance_id(sim_identifier) is None:
            return
        return super().__new__(cls)

    def _update(self, sim_identifier, *args, exclusive_base_wrapper=False, **kwargs):
        if sim_identifier.__class__ is SimInfo:
            if self._sim_info is None or self._sim_info() is None:
                self._sim_info = weakref.ref(sim_identifier)
        if sim_identifier.__class__ is Sim:
            if self._sim_instance is None or self._sim_instance() is None:
                self._sim_instance = weakref.ref(sim_identifier)

    def get_sim_id(self):
        return self._sim_id

    def get_sim_info_base(self):
        if self._sim_info_base is not None:
            return self._sim_info_base()

    def clear_sim_info_base(self):
        self._sim_info_base = None

    def get_sim_info(self):
        if self._sim_info is not None:
            sim_info = self._sim_info()
            if sim_info is not None:
                return sim_info
        sim_info = services.sim_info_manager().get(self._sim_id)
        if sim_info is None:
            return None
        self._sim_info = weakref.ref(sim_info)
        return sim_info

    def get_sim_instance(self):
        if self._sim_instance is not None:
            sim_instance = self._sim_instance()
            if sim_instance is not None:
                return sim_instance
        sim_info = self.get_sim_info()
        if sim_info is None:
            return None
        sim_instance = sim_info.get_sim_instance(allow_hidden_flags=ALL_HIDDEN_REASONS_EXCEPT_UNINITIALIZED)
        if sim_instance is None:
            return None
        self._sim_instance = weakref.ref(sim_instance)
        return sim_instance

    def get_temp_value(self, key, default=None):
        if isinstance(default, type) and issubclass(default, (dict, list, set)):
            if key not in self._temp_values:
                self._temp_values[key] = default()
            return self._temp_values.get(key, default)

    def set_temp_value(self, key, value):
        self._temp_values[key] = value

    def remove_temp_value(self, key):
        self._temp_values.pop(key, None)


def _get_sim_instance_id(sim_identifier):
    if sim_identifier is not None:
        if isinstance(sim_identifier, _SuperOmutsuSim):
            return sim_identifier.get_sim_id()
        if isinstance(sim_identifier, SimInfo) or isinstance(sim_identifier, Sim) or isinstance(sim_identifier, SimInfoBaseWrapper):
            return sim_identifier.sim_id
        if isinstance(sim_identifier, int):
            sim_info = services.sim_info_manager().get(sim_identifier)
            if sim_info is not None:
                return sim_info.sim_id
        elif isinstance(sim_identifier, str):
            if " " in sim_identifier:
                sim_name = sim_identifier.split(" ")
                sim_info = services.sim_info_manager().get_sim_info_by_name(sim_name[0], sim_name[1])
                if sim_info is not None:
                    return sim_info.sim_id
        else:
            try:
                sim_id = int(sim_identifier)
                sim_info = services.sim_info_manager().get(sim_id)
                if sim_info is not None:
                    return sim_info.sim_id
            except ValueError:
                pass
