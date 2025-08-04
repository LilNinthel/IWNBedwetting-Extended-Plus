from omutsulib.services.components_service import OmutsuComponentType, get_components_service
from omutsulib.wrappers.game_object.super_game_object import _SuperOmutsuGameObject

class _OmutsuObjectPortalMixin(_SuperOmutsuGameObject):

    def refresh_locks(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            locking_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.PORTAL_LOCKING)
            if locking_component is not None:
                locking_component.refresh_locks()
