from server.client import Client
from sims.aging.aging_mixin import AgingMixin
from sims.occult.occult_tracker import OccultTracker
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims.sim_spawner import SimSpawner
from omutsulib.events.utils.events_handler import OmutsuEventsHandler
from omutsulib.utils.injector import inject
from omutsulib.wrappers.enum import OmutsuIntEnum
from omutsulib.wrappers.sim.sim import OmutsuSim
try:
    import iwnbedwetting._debug_
    _log_timings = True if iwnbedwetting._debug_ else False
except:
    _log_timings = None

_sim_events_handler = OmutsuEventsHandler(log_timings=_log_timings)

class SimEventType(OmutsuIntEnum):
    SIM_EARLY_INIT = 1
    SIM_LATE_INIT = 2
    SIM_SPAWN = 3
    SIM_STARTUP = 4
    SIM_OCCULT_ACQUIRE = 5
    SIM_OCCULT_CHANGE = 6
    SIM_AGE_CHANGE = 7
    SIM_ACTIVE_CHANGE = 8


class OmutsuSimulationState(OmutsuIntEnum):
    INITIALIZING = 1
    RESETTING = 2
    SIMULATING = 3
    BEING_DESTROYED = 4


def register_sim_info_instance_init_event_method(unique_id=None, priority=0, early=False, late=False):

    def _method_wrapper(event_method):
        global _sim_events_handler
        if early:
            _sim_events_handler.register_event_method(priority, unique_id, event_method, event_type=(SimEventType.SIM_EARLY_INIT))
        if late:
            _sim_events_handler.register_event_method(priority, unique_id, event_method, event_type=(SimEventType.SIM_LATE_INIT))
        return event_method

    return _method_wrapper


@inject(SimInfo, "__init__")
def _iwnbedwetting_sim_info_init(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        _sim_events_handler.execute_event_methods(self, event_type=(SimEventType.SIM_EARLY_INIT))
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal method '_iwnbedwetting_sim_info_init' at 'SimInfo.__init__'.", ex)
        finally:
            ex = None
            del ex

    return result


@inject(SimInfo, "load_sim_info")
def _iwnbedwetting_sim_info_load(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        _sim_events_handler.execute_event_methods(self, event_type=(SimEventType.SIM_LATE_INIT))
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal method '_iwnbedwetting_sim_info_load' at 'SimInfo.load_sim_info'.", ex)
        finally:
            ex = None
            del ex

    return result


def register_sim_instance_spawn_event_method(unique_id=None, priority=0):

    def _method_wrapper(event_method):
        _sim_events_handler.register_event_method(priority, unique_id, event_method, event_type=(SimEventType.SIM_SPAWN))
        return event_method

    return _method_wrapper


@inject(SimSpawner, "spawn_sim")
def _iwnbedwetting_sim_instance_spawn(original, _, *args, **kwargs):
    result = original(*args, **kwargs)
    try:
        if result:
            sim_info = args[0]
            _sim_events_handler.execute_event_methods((sim_info.get_sim_instance() or sim_info), event_type=(SimEventType.SIM_SPAWN))
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal method '_iwnbedwetting_sim_instance_spawn' at 'SimSpawner.spawn_sim'.", ex)
        finally:
            ex = None
            del ex

    return result


def register_sim_startup_event_method(unique_id=None, priority=0):

    def _method_wrapper(event_method):
        _sim_events_handler.register_event_method(priority, unique_id, event_method, event_type=(SimEventType.SIM_STARTUP))
        return event_method

    return _method_wrapper


@inject(Sim, "_startup_sim_gen")
def _iwnbedwetting_sim_startup_sim_gen(original, self, *args, **kwargs):
    simulation_state = self._simulation_state
    yield from original(self, *args, **kwargs)
    try:
        _sim_events_handler.execute_event_methods(self, simulation_state, event_type=(SimEventType.SIM_STARTUP))
        if simulation_state == OmutsuSimulationState.INITIALIZING:
            omutsu_sim = OmutsuSim(self)
            if omutsu_sim is not None:
                omutsu_sim._handle_delayed_buff_on_instance_spawn()
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal method '_iwnbedwetting_sim_instance_spawn' at 'SimSpawner.spawn_sim'.", ex)
        finally:
            ex = None
            del ex

    if False:
        yield None


def register_sim_occult_type_acquire_event_method(unique_id=None, priority=0):

    def _method_wrapper(event_method):
        _sim_events_handler.register_event_method(priority, unique_id, event_method, event_type=(SimEventType.SIM_OCCULT_ACQUIRE))
        return event_method

    return _method_wrapper


@inject(OccultTracker, "add_occult_type")
def _iwnbedwetting_on_occult_type_acquire(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        sim_info = self._sim_info
        occult_type = args[0]
        _sim_events_handler.execute_event_methods(sim_info, occult_type, event_type=(SimEventType.SIM_OCCULT_ACQUIRE))
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal method '_iwnbedwetting_on_occult_type_acquire' at 'OccultTracker.add_occult_type'.", ex)
        finally:
            ex = None
            del ex

    return result


def register_sim_occult_type_change_event_method(unique_id=None, priority=0):

    def _method_wrapper(event_method):
        _sim_events_handler.register_event_method(priority, unique_id, event_method, event_type=(SimEventType.SIM_OCCULT_CHANGE))
        return event_method

    return _method_wrapper


@inject(OccultTracker, "switch_to_occult_type")
def _iwnbedwetting_on_switch_to_occult_type(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        sim_info = self._sim_info
        occult_type = args[0]
        _sim_events_handler.execute_event_methods(sim_info, occult_type, event_type=(SimEventType.SIM_OCCULT_CHANGE))
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal method '_iwnbedwetting_on_switch_to_occult_type' at 'OccultTracker.switch_to_occult_type'.", ex)
        finally:
            ex = None
            del ex

    return result


def register_sim_age_change_event_method(unique_id=None, priority=0):

    def _method_wrapper(event_method):
        _sim_events_handler.register_event_method(priority, unique_id, event_method, event_type=(SimEventType.SIM_AGE_CHANGE))
        return event_method

    return _method_wrapper


@inject(AgingMixin, "change_age")
def _iwnbedwetting_on_age_change(original, self, *args, **kwargs):
    from_age = self.age
    result = original(self, *args, **kwargs)
    try:
        to_age = args[0]
        _sim_events_handler.execute_event_methods(self, from_age, to_age, event_type=(SimEventType.SIM_AGE_CHANGE))
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal method '_iwnbedwetting_on_age_change' at 'AgingMixin.change_age'.", ex)
        finally:
            ex = None
            del ex

    return result


def register_sim_active_change_event_method(unique_id=None, priority=0):

    def _method_wrapper(event_method):
        _sim_events_handler.register_event_method(priority, unique_id, event_method, event_type=(SimEventType.SIM_ACTIVE_CHANGE))
        return event_method

    return _method_wrapper


@inject(Client, "notify_active_sim_changed")
def _iwnbedwetting_on_active_sim_change(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        old_sim_instance = args[0]
        if old_sim_instance is not None:
            old_sim_info = old_sim_instance.sim_info
        else:
            old_sim_info = None
        new_sim_info = kwargs.get("new_sim_info", None)
        _sim_events_handler.execute_event_methods(old_sim_info, new_sim_info, event_type=(SimEventType.SIM_ACTIVE_CHANGE))
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal method '_iwnbedwetting_on_active_sim_change' at 'Client.notify_active_sim_changed'.", ex)
        finally:
            ex = None
            del ex

    return result
