import time
from omutsulib.wrappers.logger import OmutsuLogger

class OmutsuEventsHandler:

    def __init__(self, log_timings=False):
        self._event_handlers = {}
        self._event_handlers_to_unregister = []
        self.timings_logger = OmutsuLogger("OmutsuEventsHandler") if log_timings else None

    def register_event_method(self, priority, unique_id, event_method, event_type=0):
        if unique_id is None or event_method is None:
            return
        handlers_list = [] if event_type not in self._event_handlers else self._event_handlers[event_type]
        handlers_list.append((priority, unique_id, event_method))
        handlers_list = sorted(handlers_list, key=(lambda x: x[0]))
        self._event_handlers[event_type] = handlers_list
        if self.timings_logger is not None:
            self.timings_logger.info("Registered Event Handler of '{}' named '{}' (ID: {}).".format(unique_id, event_method.__name__, event_type))
        return True

    def unregister_event_method(self, unique_id, event_method_or_name, event_type=0):
        event_method_name = event_method_or_name if isinstance(event_method_or_name, str) else event_method_or_name.__name__
        self._event_handlers_to_unregister.append((unique_id, event_method_name, event_type))
        return True

    def _unregister_event_methods(self):
        if self._event_handlers_to_unregister:
            for (unique_id, event_method_name, event_type) in self._event_handlers_to_unregister:
                if event_type in list(self._event_handlers):
                    handlers_list = self._event_handlers[event_type]
                    for entry in handlers_list:
                        (_, handler_unique_id, event_method) = entry
                        if handler_unique_id == unique_id:
                            if event_method.__name__ == event_method_name:
                                handlers_list.remove(entry)
                                if self.timings_logger is not None:
                                    self.timings_logger.info("Unregistered Event Handler of '{}' named '{}' (ID: {}).".format(unique_id, event_method.__name__, event_type))

            self._event_handlers_to_unregister.clear()

    def execute_event_methods(self, *args, event_type=0):
        if event_type not in self._event_handlers:
            return False
        self._unregister_event_methods()
        handlers_list = self._event_handlers[event_type]
        for (_, handler_unique_id, event_method) in handlers_list:
            try:
                if self.timings_logger is not None:
                    ts = time.perf_counter()
                    event_method(*args)
                    self.timings_logger.info("Event Handler of '{}' run '{}' (ID: {}) for {}s.".format(handler_unique_id, event_method.__name__, event_type, "%.8f" % (time.perf_counter() - ts)))
                else:
                    event_method(*args)
            except Exception as ex:
                try:
                    pass  # log_custom_exception("[OmutsuLib] Failed to run '{}' method from '{}'".format(event_method.__name__, handler_unique_id), ex)
                finally:
                    ex = None
                    del ex

        return True

    def execute_event_methods_gen(self, *args, event_type=0):
        if event_type in self._event_handlers:
            self._unregister_event_methods()
            handlers_list = self._event_handlers[event_type]
            for (_, handler_unique_id, event_method) in handlers_list:
                try:
                    yield event_method(*args)
                except Exception as ex:
                    try:
                        pass  # log_custom_exception("[OmutsuLib] Failed to run '{}' method from '{}'".format(event_method.__name__, handler_unique_id), ex)
                    finally:
                        ex = None
                        del ex
