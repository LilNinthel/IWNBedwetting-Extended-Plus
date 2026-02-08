from omutsulib.services.components_service import get_components_service, OmutsuComponentType
from omutsulib.wrappers.game_object.super_game_object import _SuperOmutsuGameObject

class _OmutsuObjectNameMixin(_SuperOmutsuGameObject):

    def get_custom_name(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            name_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.NAME)
            if name_component:
                return object_instance.custom_name

    def set_custom_name(self, name, actor_sim_id=None):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            name_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.NAME)
            if name_component:
                name_component.set_custom_name(name, actor_sim_id=actor_sim_id)

    def get_custom_description(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            name_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.NAME)
            if name_component:
                return object_instance.custom_description

    def set_custom_description(self, description, force_set=False, update_tooltip=True):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            name_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.NAME)
            if name_component:
                name_component.set_custom_description(description, force_set=force_set, update_tooltip=update_tooltip)
