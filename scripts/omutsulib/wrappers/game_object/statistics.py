from omutsulib.wrappers.game_object.super_game_object import _SuperOmutsuGameObject

class _OmutsuObjectStatisticsMixin(_SuperOmutsuGameObject):

    def has_statistic(self, statistic_id, combined=False):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            if not combined:
                return self._get_statistics_service().has_statistic(object_instance, statistic_id)
            return self._get_combined_statistics_service().has_statistic(object_instance, statistic_id)
        return False

    def remove_statistic(self, statistic_id, combined=False):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            if not combined:
                self._get_statistics_service().remove_statistic(object_instance, statistic_id)
            else:
                self._get_combined_statistics_service().remove_statistic(object_instance, statistic_id)

    def clear_statistic(self, statistic_id):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            self._get_statistics_service().clear_statistic(object_instance, statistic_id)

    def set_statistic_value(self, statistic_id, value, add=True, combined=False):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            if not combined:
                self._get_statistics_service().set_statistic_value(object_instance, statistic_id, value, add=add)
            else:
                self._get_combined_statistics_service().set_statistic_value(object_instance, statistic_id, value, add=add)

    def change_statistic_value(self, statistic_id, value, add=True):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            self._get_statistics_service().change_statistic_value(object_instance, statistic_id, value, add=add)

    def get_statistic_value(self, statistic_id, add=False, combined=False, default=0):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            if not combined:
                return self._get_statistics_service().get_statistic_value(object_instance, statistic_id, add=add, default=default)
            return self._get_combined_statistics_service().get_statistic_value(object_instance, statistic_id, add=add, default=default)
        return default

    def add_statistic_modifier(self, statistic_id, modifier_value, add=False):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            self._get_statistics_service().add_statistic_modifier(object_instance, statistic_id, modifier_value, add=add)

    def remove_statistic_modifier(self, statistic_id, modifier_value, add=False):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            self._get_statistics_service().remove_statistic_modifier(object_instance, statistic_id, modifier_value, add=add)

    def clear_statistic_modifiers(self, statistic_id, add=False):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            self._get_statistics_service().clear_statistic_modifiers(object_instance, statistic_id, add=add)

    def is_statistic_locked(self, statistic_id):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return self._get_statistics_service().is_statistic_locked(object_instance, statistic_id)
        return False

    def get_statistic_locked_count(self, statistic_id):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return self._get_statistics_service().get_statistic_locked_count(object_instance, statistic_id)
        return 0

    def lock_statistic(self, statistic_id, **kwargs):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return (self._get_statistics_service().lock_statistic)(object_instance, statistic_id, **kwargs)
        return False

    def unlock_statistic(self, statistic_id, **kwargs):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return (self._get_statistics_service().unlock_statistic)(object_instance, statistic_id, **kwargs)
        return False

    def add_statistic_watcher(self, callback):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return self._get_statistics_service().add_statistic_watcher(object_instance, callback)

    def remove_statistic_watcher(self, handle_id):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            self._get_statistics_service().remove_statistic_watcher(object_instance, handle_id)

    def _get_statistics_service(self):
        from omutsulib.services.statistics_service import get_statistics_service
        return get_statistics_service()

    def _get_combined_statistics_service(self):
        from omutsulib.services.combined_statistics_service import get_combined_statistics_service
        return get_combined_statistics_service()

    def register_on_statistic_removed_callback(self, callback):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            commodity_tracker = object_instance.commodity_tracker
            if commodity_tracker is not None:
                if commodity_tracker._on_remove_callbacks is None or callback not in commodity_tracker._on_remove_callbacks:
                    commodity_tracker.add_on_remove_callback(callback)
                    return True
            return False

    def unregister_on_statistic_removed_callback(self, callback):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            commodity_tracker = object_instance.commodity_tracker
            if commodity_tracker is not None:
                commodity_tracker.remove_on_remove_callback(callback)
                return True
            return False
