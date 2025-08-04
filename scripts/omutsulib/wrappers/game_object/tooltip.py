from omutsulib.services.components_service import get_components_service, OmutsuComponentType
from omutsulib.wrappers.game_object.super_game_object import _SuperOmutsuGameObject

class _OmutsuObjectTooltipMixin(_SuperOmutsuGameObject):

    def update_tooltip(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            tooltip_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.TOOLTIP)
            if tooltip_component is not None:
                tooltip_component.update_object_tooltip()
