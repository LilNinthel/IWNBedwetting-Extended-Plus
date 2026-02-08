import math, services
from clock import ClockSpeedMode
from zone import Zone
from omutsulib.utils.injector import inject
_last_absolute_ticks = 0
_current_diff_ticks = 0
_diff_ticks_error = 0
_last_diff_ticks_average = [
 35] * 30
_diff_ticks_average = 35
_on_zone_update_methods = []

def get_current_diff_ticks():
    global _current_diff_ticks
    return _current_diff_ticks


def get_current_diff_ticks_average():
    global _diff_ticks_average
    return _diff_ticks_average


def register_zone_update_event_method(unique_id=None, always_run=False):

    def _method_wrapper(event_method):
        manual_register_zone_update_event_method(event_method, unique_id=unique_id, always_run=always_run)
        return event_method

    return _method_wrapper


def manual_register_zone_update_event_method(update_method, unique_id=None, always_run=False):
    global _on_zone_update_methods
    _on_zone_update_methods.append(ZoneUpdateHandler(unique_id, update_method, always_run=always_run))


def manual_unregister_zone_update_event_method(update_method, unique_id=None):
    for zone_update_handler in _on_zone_update_methods:
        if zone_update_handler.get_unique_id() == unique_id:
            if zone_update_handler.get_update_method() == update_method:
                _on_zone_update_methods.remove(zone_update_handler)
                return

    raise ValueError("Failed to unregister a Zone Update Event {} method. ({})".format(update_method.__name__, unique_id))


class ZoneUpdateHandler:

    def __init__(self, unique_id, update_method, always_run=False):
        self.unique_id = unique_id
        self.update_method = update_method
        self.always_run = always_run

    def get_unique_id(self):
        return self.unique_id

    def get_update_method(self):
        return self.update_method

    def update(self):
        self.update_method()


@inject(Zone, "update")
def _iwnbedwetting_zone_game_update(original, self, *args, **kwargs):
    global _current_diff_ticks
    global _diff_ticks_average
    global _diff_ticks_error
    global _last_absolute_ticks
    global _last_diff_ticks_average
    result = original(self, *args, **kwargs)
    try:
        if self.is_zone_running:
            absolute_ticks = args[0]
            is_paused = services.game_clock_service().clock_speed == ClockSpeedMode.PAUSED
            if not is_paused:
                diff_ticks = absolute_ticks - _last_absolute_ticks
                if diff_ticks < 0:
                    return result
                if diff_ticks > 5000:
                    diff_ticks = 5000
                ideal_diff_ticks = diff_ticks * services.game_clock_service().current_clock_speed_scale() + _diff_ticks_error
                rounded_ticks = math.floor(ideal_diff_ticks + 0.5)
                ticks_error = ideal_diff_ticks - rounded_ticks
                _diff_ticks_error = max(min(ticks_error, 1), -1)
                _current_diff_ticks = rounded_ticks
                _last_diff_ticks_average.append(rounded_ticks)
                _last_diff_ticks_average.pop(0)
                _diff_ticks_average = int(sum(_last_diff_ticks_average) / len(_last_diff_ticks_average))
            _last_absolute_ticks = absolute_ticks
            _on_zone_update_event(is_paused)
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run internal method '_iwnbedwetting_zone_game_update' at 'Zone.update'.", ex)
        finally:
            ex = None
            del ex

    return result


def _on_zone_update_event(is_paused):
    for zone_update_handler in _on_zone_update_methods:
        try:
            if not is_paused or zone_update_handler.always_run:
                zone_update_handler.update()
        except Exception as ex:
            try:
                pass  # log_custom_exception("[OmutsuLib] Failed to run '{}' method from '{}'.".format(zone_update_handler.get_update_method().__name__, zone_update_handler.unique_id), ex)
            finally:
                ex = None
                del ex
