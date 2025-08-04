from _weakrefset import WeakSet
from collections import OrderedDict
from functools import wraps
from omutsulib.events.zone_spin import has_game_loaded
from omutsulib.services.persistence_service import get_persistence_service
from omutsulib.services.time_service import get_time_service
_cache_wrappers = WeakSet()

def clear_cached_returns(identifier=None):
    global _cache_wrappers
    for cache_wrapper in _cache_wrappers:
        if not identifier is None:
            if cache_wrapper.identifier == identifier:
                pass
            cache_wrapper.cache.clear()


def cache_return(cache_max_size=100, identifier=None, expiration=None, validation_fn=None):

    def cached_function(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = wrapper.cache
            if wrapper.control_value != _get_control_value():
                wrapper.control_value = _get_control_value()
                cache.clear()
            if wrapper.expiration is not None:
                if get_time_service().get_absolute_ticks() > wrapper.last_absolute_tick + wrapper.expiration:
                    wrapper.last_absolute_tick = get_time_service().get_absolute_ticks()
                    cache.clear()
                validation_value = (wrapper.validation_fn)(*args, **kwargs) if wrapper.validation_fn is not None else None
                if validation_value != wrapper.validation_value:
                    wrapper.validation_value = validation_value
                    cache.clear()
                signature = None
                try:
                    signature = (args, frozenset(kwargs.items()))
                    result = cache[signature]
                except TypeError as ex:
                    try:
                        raise ex
                    finally:
                        ex = None
                        del ex

                except KeyError:
                    result = func(*args, **kwargs)
                    cache[signature] = result

                if cache_max_size != -1:
                    if len(cache) > cache_max_size:
                        cache.popitem(last=False)
                return result

        wrapper.identifier = identifier
        wrapper.expiration = expiration
        wrapper.last_absolute_tick = 0
        wrapper.validation_fn = validation_fn
        wrapper.validation_value = None
        wrapper.cache = OrderedDict()
        wrapper.control_value = _get_control_value()
        wrapper.original_function = func
        _cache_wrappers.add(wrapper)
        return wrapper

    return cached_function


def _get_control_value():
    if not has_game_loaded():
        return 0
    return (
     get_persistence_service().get_save_slot_guid(), get_persistence_service().get_save_slot_id())
