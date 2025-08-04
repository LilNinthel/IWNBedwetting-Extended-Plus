from omutsulib.services.components_service import get_components_service, OmutsuComponentType
from omutsulib.utils.math import Location, SurfaceIdentifier
from omutsulib.utils.singletons import ZERO_VECTOR3, ZERO_TRANSFORM
from omutsulib.wrappers.game_object.super_game_object import _SuperOmutsuGameObject


class _OmutsuObjectLocationMixin(_SuperOmutsuGameObject):

    def set_location(self, location):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            object_instance.location = location

    def get_location(self, absolute=True):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            if absolute:
                parent_object_instance = object_instance.parent_object()
                if parent_object_instance is not None:
                    if parent_object_instance is not object_instance:
                        return object_instance.location.clone(transform=(object_instance.transform),
                                                              routing_surface=(parent_object_instance.routing_surface),
                                                              parent=None)
                    return object_instance.location
            return Location(ZERO_VECTOR3, 0, 0.0)

    def get_location_parent(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.location.parent

    def get_transform(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.transform
        return ZERO_TRANSFORM

    def get_position(self, bone_name=None):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            if bone_name is not None:
                try:
                    return object_instance.get_joint_transform_for_joint(bone_name).translation
                except:
                    pass

                return object_instance.position
            return ZERO_VECTOR3

    def get_forward_vector(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.forward
        return ZERO_VECTOR3

    def get_orientation(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.orientation
        return 0.0

    def get_routing_surface(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.routing_surface
        return SurfaceIdentifier(0)

    def get_level(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            if object_instance.routing_surface:
                return object_instance.routing_surface.secondary_id
            return 0
        return 0

    def set_live_drag_state(self, can_live_drag):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            live_drag_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.LIVE_DRAG)
            if live_drag_component is not None:
                live_drag_component._set_can_live_drag(can_live_drag)
