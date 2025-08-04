from typing import TYPE_CHECKING
import sims4.hash_util
from carry.carry_postures import CarryingObject
from objects import MaterialState
from objects.object_enums import ResetReason
from native_enums.tags_enum import NativeGameTag
from omutsulib.services.world_service import get_zone_service
from omutsulib.wrappers.game_object.super_game_object import _SuperOmutsuGameObject
if TYPE_CHECKING:
    from omutsulib.wrappers.game_object.game_object import OmutsuGameObject

class OmutsuPersistenceGroup:
    NONE = 0
    OBJECT = 1
    SIM = 2
    IN_OPEN_STREET = 3


class OmutsuPostureTransitionTargetPreferenceTag:
    INVALID = -1
    DINING_TABLE = 0
    SINK_COUNTER = 1
    SINK_PEDESTAL = 2
    SEATING_DINING = 3
    SEATING_LOVESEAT = 4
    SEATING_LIVING = 5
    SEATING_DESK = 6
    SEATING_SOFA = 7
    SEATING_BED = 8
    SEATING_BARSTOOL = 9
    SURFACE_DESK = 10
    SURFACE_COUNTER = 11
    SURFACE_BAR = 12
    SEATING_POOL = 13
    SEATING_TOILET = 14
    INTERROGATION_TABLE = 15
    BOOKING_STATION = 16
    CELL_DOOR = 17
    SEATING_ROCK = 18
    SEATING_SWINGS = 19
    BUNNYSLOPE_EASY = 20
    SEATING_HOTTUB = 21


class OmutsuVisibilityFlags:
    MIRRORS = 1
    LOT_WATER_REFLECTION = 2
    WORLD_WATER_REFLECTION = 4


class _OmutsuObjectInternalMixin(_SuperOmutsuGameObject):

    def is_available(self: "OmutsuGameObject"):
        if get_zone_service().is_position_at_inactive_plex(self.get_position(), self.get_level()):
            return False
        if get_zone_service().is_current_zone_a_plex() and NativeGameTag.BUILD_WINDOW in self.get_game_tags():
            inside_position = self.get_position() - self.get_forward_vector()
            if get_zone_service().is_position_at_inactive_plex(inside_position, self.get_level()):
                return False
            outside_position = self.get_position() + self.get_forward_vector()
            if get_zone_service().is_position_at_inactive_plex(outside_position, self.get_level()):
                return False
            return True

    def get_catalog_name(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.catalog_name

    def is_in_inventory(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.is_in_inventory()
        return False

    def is_in_world(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return not object_instance.is_in_inventory() and object_instance.routing_surface is not None
        return False

    def has_parent(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            parent_object_instance = object_instance.parent_object()
            return parent_object_instance is not None and parent_object_instance is not object_instance
        return False

    def get_parent(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            parent_object_instance = object_instance.parent_object()
            if parent_object_instance is not None:
                if parent_object_instance is not object_instance:
                    while parent_object_instance is not None:
                        parent = parent_object_instance.parent_object()
                        if parent is not None:
                            parent_object_instance = parent
                        else:
                            break

                    object_instance = parent_object_instance
                from omutsulib.wrappers.game_object.game_object import OmutsuGameObject
                return OmutsuGameObject(object_instance)

    def set_parent(self, parent_object_instance, joint_name_or_hash=None, **kwargs):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            joint_name_hash = sims4.hash_util.hash32(joint_name_or_hash) if isinstance(joint_name_or_hash, str) else joint_name_or_hash
            (object_instance.set_parent)(parent_object_instance, joint_name_or_hash=joint_name_hash, **kwargs)

    def clear_parent(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            parent_object_instance = object_instance.get_parenting_root()
            if parent_object_instance is not None:
                object_instance.clear_parent(object_instance.transform, parent_object_instance.routing_surface)

    def get_posture_transition_target_tag(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.posture_transition_target_tag
        return OmutsuPostureTransitionTargetPreferenceTag.INVALID

    def get_visibility_flags(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            visibility_flags = object_instance.visibility_flags
            if visibility_flags is not None:
                return visibility_flags
            return 255

    def set_visibility_flags(self, value):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            object_instance.visibility_flags = value

    def fade_in(self, fade_duration=1.0, immediate=False):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            object_instance.fade_in(fade_duration=fade_duration, immediate=immediate)

    def fade_out(self, fade_duration=1.0, immediate=False):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            object_instance.fade_out(fade_duration=fade_duration, immediate=immediate)

    def get_scale(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.scale

    def set_scale(self, value):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            object_instance.scale = value

    def get_persistence_group(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.persistence_group

    def set_persistence_group(self, persistence_group):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            object_instance.persistence_group = persistence_group

    def get_geometry_state(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.geometry_state
        return 0

    def set_geometry_state(self, state_value):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            object_instance.geometry_state = state_value

    def get_material_state(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            material_state = object_instance.material_state
            if material_state is not None:
                return material_state.debug_state_name
            return ""

    def set_material_state(self, state_value, opacity=1.0, transition=0.0):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            if state_value is None:
                object_instance.material_state = None
            else:
                object_instance.material_state = MaterialState(state_value, opacity=opacity, transition=transition)

    def remove_from_client(self, **kwargs):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            (object_instance.remove_from_client)(**kwargs)

    def destroy(self, schedule=False, cause=None, **kwargs):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            if schedule:
                (object_instance.schedule_destroy_asap)(cause=cause, **kwargs)
            else:
                (object_instance.destroy)(cause=cause, **kwargs)

    def hard_reset(self):
        object_instance = self.get_object_instance()
        if object_instance is None:
            return True
        try:
            object_instance.reset(ResetReason.RESET_EXPECTED)
            return True
        except:
            return False

    def soft_reset(self, hard_reset_on_exception=False):
        object_instance = self.get_object_instance()
        if object_instance is None:
            return True
        try:
            if object_instance.parent is not None and object_instance.parent.is_sim:
                if not object_instance.parent.posture_state.is_carrying(object_instance):
                    CarryingObject.snap_to_good_location_on_floor(object_instance, starting_transform=(object_instance.parent.transform), starting_routing_surface=(object_instance.parent.routing_surface))
                location = object_instance.location
                object_instance.on_reset_send_op(ResetReason.RESET_EXPECTED)
                object_instance.location = location
                object_instance.resend_location()
                if object_instance.routing_component is not None:
                    object_instance.routing_component.on_reset_internal_state()
                if object_instance.idle_component is not None:
                    object_instance.idle_component._refresh_active_idle()
                if object_instance.linked_object_component is not None:
                    object_instance.linked_object_component._relink(update_others=True)
            return True
        except:
            if hard_reset_on_exception:
                return self.hard_reset()

        return False

    def is_visible(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            if object_instance.is_hidden() or object_instance.opacity == 0:
                return False
            return True
