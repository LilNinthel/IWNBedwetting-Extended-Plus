from omutsulib.services.components_service import get_components_service, OmutsuComponentType
from omutsulib.services.resources_service import get_resource_service, OmutsuResourceType
from omutsulib.wrappers.game_object.super_game_object import _SuperOmutsuGameObject

class _OmutsuObjectStateMixin(_SuperOmutsuGameObject):

    def remove_state(self, state_identifier):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            state_instance = get_resource_service().get_instance(OmutsuResourceType.OBJECT_STATE, state_identifier)
            if state_instance is not None:
                state_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.STATE)
                if state_component is not None:
                    return state_component._states.pop(state_instance, None)

    def set_state_value(self, state_value_id, immediate=False, force_update=False, **kwargs):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            state_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.STATE)
            if state_component is not None:
                state_value_instance = get_resource_service().get_instance(OmutsuResourceType.OBJECT_STATE, state_value_id)
                if state_value_instance is not None:
                    (state_component.set_state)(state_value_instance.state, state_value_instance, immediate=immediate, force_update=force_update, **kwargs)

    def get_state_value(self, state_identifier):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            state_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.STATE)
            if state_component is not None:
                return next(iter((state_value for (object_state, state_value) in state_component.items())), None)

    def get_state_values(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            state_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.STATE)
            if state_component is not None:
                return tuple(state_component.values())
            return ()

    def has_state_value(self, *state_value_ids):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            state_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.STATE)
            if state_component is not None:
                object_state_value_ids = {state_value.guid64 for state_value in state_component.values()}
                return not set(state_value_ids).isdisjoint(object_state_value_ids)
            return False

    def get_state_commodity_value(self, state_identifier):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            state_instance = get_resource_service().get_instance(OmutsuResourceType.OBJECT_STATE, state_identifier)
            if state_instance is not None:
                state_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.STATE)
                if state_component is not None:
                    statistic_instance = state_instance.linked_stat
                    if statistic_instance is not None:
                        if statistic_instance in state_component._commodity_states:
                            tracker = state_component._get_tracker(state_instance)
                            if tracker is not None:
                                return tracker.get_value(statistic_instance)
                            if hasattr(statistic_instance, "get_initial_value"):
                                return statistic_instance.get_initial_value()
                            return statistic_instance.default_value
            return 0

    def set_state_commodity_value(self, state_id, value):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            state_instance = get_resource_service().get_instance(OmutsuResourceType.OBJECT_STATE, state_id)
            if state_instance is not None:
                state_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.STATE)
                if state_component is not None:
                    statistic_instance = state_instance.linked_stat
                    if statistic_instance is not None:
                        if statistic_instance in state_component._commodity_states:
                            tracker = state_component._get_tracker(state_instance)
                            if tracker is not None:
                                tracker.set_value(statistic_instance, value, add=True, from_init=False)
