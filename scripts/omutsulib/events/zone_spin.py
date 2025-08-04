from services.persistence_service import PersistenceService
from omutsulib.events.utils.events_handler import OmutsuEventsHandler
from omutsulib.utils.injector import inject
from omutsulib.wrappers.enum import OmutsuIntEnum
from zone import Zone
from zone_manager import ZoneManager
try:
    import iwnbedwetting._debug_
    _log_timings = True if iwnbedwetting._debug_ else False
except:
    _log_timings = None

_has_game_loaded = False
_is_game_loading = True
_core_events_handler = OmutsuEventsHandler(log_timings=_log_timings)

class CoreEventType(OmutsuIntEnum):
    ZONE_EARLY_LOAD = 1
    ZONE_LATE_LOAD = 2
    ZONE_LOADING_SCREEN_FINISH = 3
    ZONE_PRE_SAVE = 4
    ZONE_POST_SAVE = 5
    ZONE_TEARDOWN = 6


def has_game_loaded():
    global _has_game_loaded
    return _has_game_loaded


def is_game_loading():
    global _is_game_loading
    return _is_game_loading


def register_zone_load_event_method(unique_id=None, priority=0, early=False, late=False, loading_screen=False):

    def _method_wrapper(event_method):
        global _core_events_handler
        if early:
            _core_events_handler.register_event_method(priority, unique_id, event_method, event_type=(CoreEventType.ZONE_EARLY_LOAD))
        if late:
            _core_events_handler.register_event_method(priority, unique_id, event_method, event_type=(CoreEventType.ZONE_LATE_LOAD))
        if loading_screen:
            _core_events_handler.register_event_method(priority, unique_id, event_method, event_type=(CoreEventType.ZONE_LOADING_SCREEN_FINISH))
        return event_method

    return _method_wrapper


def unregister_zone_load_event_method(event_method_or_name, unique_id=None, early=False, late=False):
    if early:
        if not _core_events_handler.unregister_event_method(unique_id, event_method_or_name, CoreEventType.ZONE_EARLY_LOAD):
            raise ValueError("Failed to unregister a Zone Load Event {} early method. ({})".format(event_method_or_name.__name__, unique_id))
        if late and not _core_events_handler.unregister_event_method(unique_id, event_method_or_name, CoreEventType.ZONE_LATE_LOAD):
            raise ValueError("Failed to unregister a Zone Load Event {} late method. ({})".format(event_method_or_name.__name__, unique_id))


@inject(Zone, "load_zone")
def _iwnbedwetting_on_early_zone_load(original, self, *args, **kwargs):
    try:
        result = original(self, *args, **kwargs)
    except:
        result = None

    try:
        _core_events_handler.execute_event_methods(event_type=(CoreEventType.ZONE_EARLY_LOAD))
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal method '_iwnbedwetting_on_early_zone_load' at 'Zone.load_zone'.", ex)
        finally:
            ex = None
            del ex

    return result


@inject(Zone, "do_zone_spin_up")
def _iwnbedwetting_on_late_zone_load(original, self, *args, **kwargs):
    global _has_game_loaded
    global _is_game_loading
    try:
        result = original(self, *args, **kwargs)
    except:
        result = None

    try:
        _core_events_handler.execute_event_methods(event_type=(CoreEventType.ZONE_LATE_LOAD))
        _has_game_loaded = True
        _is_game_loading = False
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal method '_iwnbedwetting_on_late_zone_load' at 'Zone.do_zone_spin_up'.", ex)
        finally:
            ex = None
            del ex

    return result


@inject(Zone, "on_loading_screen_animation_finished")
def _iwnbedwetting_on_loading_screen_finished(original, self, *args, **kwargs):
    try:
        result = original(self, *args, **kwargs)
    except:
        result = None

    try:
        _core_events_handler.execute_event_methods(event_type=(CoreEventType.ZONE_LOADING_SCREEN_FINISH))
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal method '_iwnbedwetting_on_loading_screen_finished' at 'Zone.on_loading_screen_animation_finished'.", ex)
        finally:
            ex = None
            del ex

    return result


def register_zone_teardown_event(unique_id=None, priority=0):

    def _method_wrapper(event_method):
        _core_events_handler.register_event_method(priority, unique_id, event_method, event_type=(CoreEventType.ZONE_TEARDOWN))
        return event_method

    return _method_wrapper


def unregister_zone_teardown_event(event_method_or_name, unique_id=None):
    if not _core_events_handler.unregister_event_method(unique_id, event_method_or_name, CoreEventType.ZONE_TEARDOWN):
        raise ValueError("Failed to unregister a Zone Teardown Event {} method. ({})".format(event_method_or_name.__name__, unique_id))


@inject(Zone, "on_teardown")
def _iwnbedwetting_on_zone_teardown(original, self, *args, **kwargs):
    global _is_game_loading
    try:
        _core_events_handler.execute_event_methods(event_type=(CoreEventType.ZONE_TEARDOWN))
        _is_game_loading = True
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal method '_iwnbedwetting_on_zone_teardown' at 'Zone.on_teardown'.", ex)
        finally:
            ex = None
            del ex

    return original(self, *args, **kwargs)


def register_zone_save_event(unique_id=None, priority=0, pre=False, post=False):

    def _method_wrapper(event_method):
        if pre:
            _core_events_handler.register_event_method(priority, unique_id, event_method, event_type=(CoreEventType.ZONE_PRE_SAVE))
        if post:
            _core_events_handler.register_event_method(priority, unique_id, event_method, event_type=(CoreEventType.ZONE_POST_SAVE))
        return event_method

    return _method_wrapper


def unregister_zone_save_event(event_method_or_name, unique_id=None, pre=False, post=False):
    if pre:
        if not _core_events_handler.unregister_event_method(unique_id, event_method_or_name, CoreEventType.ZONE_PRE_SAVE):
            raise ValueError("Failed to unregister a Zone Pre Save Event {} method. ({})".format(event_method_or_name.__name__, unique_id))
        if post and not _core_events_handler.unregister_event_method(unique_id, event_method_or_name, CoreEventType.ZONE_POST_SAVE):
            raise ValueError("Failed to unregister a Zone Post Save Event {} method. ({})".format(event_method_or_name.__name__, unique_id))


@inject(ZoneManager, "save")
def _iwnbedwetting_on_zone_pre_save(original, self, *args, **kwargs):
    try:
        _core_events_handler.execute_event_methods(event_type=(CoreEventType.ZONE_PRE_SAVE))
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal pre method '_iwnbedwetting_on_zone_pre_save' at 'ZoneManager.save'.", ex)
        finally:
            ex = None
            del ex

    try:
        return original(self, *args, **kwargs)
    except:
        return


@inject(PersistenceService, "_destroy_save_timeline")
def _iwnbedwetting_persistence_post_save_timeline_destroy(original, self, *args, **kwargs):
    try:
        timeline = args[0]
        if self.save_timeline is not None:
            if self.save_timeline is timeline:
                _core_events_handler.execute_event_methods(event_type=(CoreEventType.ZONE_POST_SAVE))
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal post method '_iwnbedwetting_on_zone_save' at 'Zone.save_zone'.", ex)
        finally:
            ex = None
            del ex

    return original(self, *args, **kwargs)
