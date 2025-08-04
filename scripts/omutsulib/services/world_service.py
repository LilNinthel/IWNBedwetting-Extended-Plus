import _buildbuy, build_buy, placement, routing, services
import sims4.math as smath
import terrain
from placement import FGLSearchFlag, FGLSearchFlagsDefault, FGLSearchFlagsDefaultForObject, FGLSearchFlagsDefaultForSim
from omutsulib.services.l18n_service import get_l18n_service
from omutsulib.services.resources_service import get_resource_service, OmutsuResourceType
from omutsulib.services.service import OmutsuService
from omutsulib.utils.math import Location, convert_orientation_to_angle

class OmutsuDynamicAreaType:
    INVALID = -1
    BUSINESS_RESIDENTIAL = 0
    BUSINESS_PUBLIC = 1
    BUSINESS_EMPLOYEES_ONLY = 2


class OmutsuFGLSearchFlag:
    USE_RANDOM_WEIGHTING = FGLSearchFlag.USE_RANDOM_WEIGHTING
    USE_RANDOM_ORIENTATION = FGLSearchFlag.USE_RANDOM_ORIENTATION
    CONTAINS_NOWHERE_CONSTRAINT = FGLSearchFlag.CONTAINS_NOWHERE_CONSTRAINT
    CONTAINS_ANYWHERE_CONSTRAINT = FGLSearchFlag.CONTAINS_ANYWHERE_CONSTRAINT
    ALLOW_TOO_CLOSE_TO_OBSTACLE = FGLSearchFlag.ALLOW_TOO_CLOSE_TO_OBSTACLE
    ALLOW_GOALS_IN_SIM_POSITIONS = FGLSearchFlag.ALLOW_GOALS_IN_SIM_POSITIONS
    ALLOW_GOALS_IN_SIM_INTENDED_POSITIONS = FGLSearchFlag.ALLOW_GOALS_IN_SIM_INTENDED_POSITIONS
    SHOULD_TEST_ROUTING = FGLSearchFlag.SHOULD_TEST_ROUTING
    SHOULD_TEST_BUILDBUY = FGLSearchFlag.SHOULD_TEST_BUILDBUY
    USE_SIM_FOOTPRINT = FGLSearchFlag.USE_SIM_FOOTPRINT
    STAY_IN_SAME_CONNECTIVITY_GROUP = FGLSearchFlag.STAY_IN_SAME_CONNECTIVITY_GROUP
    STAY_IN_CONNECTED_CONNECTIVITY_GROUP = FGLSearchFlag.STAY_IN_CONNECTED_CONNECTIVITY_GROUP
    STAY_IN_CURRENT_BLOCK = FGLSearchFlag.STAY_IN_CURRENT_BLOCK
    STAY_OUTSIDE = FGLSearchFlag.STAY_OUTSIDE
    ALLOW_INACTIVE_PLEX = FGLSearchFlag.ALLOW_INACTIVE_PLEX
    SHOULD_RAYTEST = FGLSearchFlag.SHOULD_RAYTEST
    SPIRAL_INWARDS = FGLSearchFlag.SPIRAL_INWARDS
    STAY_IN_LOT = FGLSearchFlag.STAY_IN_LOT
    ENCLOSED_ROOM_ONLY = FGLSearchFlag.ENCLOSED_ROOM_ONLY
    LOT_TERRAIN_ONLY = FGLSearchFlag.LOT_TERRAIN_ONLY
    CALCULATE_RESULT_TERRAIN_HEIGHTS = FGLSearchFlag.CALCULATE_RESULT_TERRAIN_HEIGHTS
    DONE_ON_MAX_RESULTS = FGLSearchFlag.DONE_ON_MAX_RESULTS


OmutsuFGLSearchFlagsDefault = FGLSearchFlagsDefault
OmutsuFGLSearchFlagsDefaultForObject = FGLSearchFlagsDefaultForObject
OmutsuFGLSearchFlagsDefaultForSim = FGLSearchFlagsDefaultForSim

class OmutsuWorldService(OmutsuService):

    def get_current_region(self):
        return services.current_region_instance()

    def get_region_instance(self, region_guid):
        region_tuning = get_resource_service().get_instance(OmutsuResourceType.REGION, region_guid)
        return services.region_service().get_region_instance_by_tuning(region_tuning)

    def get_current_world_id(self):
        return services.get_persistence_service().get_world_id_from_zone(services.current_zone_id())

    def get_current_world_description_id(self):
        return services.get_world_description_id(services.get_persistence_service().get_world_id_from_zone(services.current_zone_id()))

    def get_all_neighborhood_proto_buffs(self):
        return dict(((neighborhood_proto.neighborhood_id, neighborhood_proto) for neighborhood_proto in services.get_persistence_service().get_neighborhoods_proto_buf_gen()))


class OmutsuZoneService(OmutsuService):

    def get_current_zone(self):
        return services.current_zone()

    def get_current_zone_id(self):
        return services.current_zone_id()

    def get_current_zone_plex_id(self):
        return services.get_plex_service().get_active_zone_plex_id() or 0

    def is_current_zone_a_plex(self):
        return services.get_plex_service().is_active_zone_a_plex()

    def get_zone_plex_id_at_position(self, position, level):
        plex_service = services.get_plex_service()
        if plex_service.is_active_zone_a_plex():
            return plex_service.get_plex_zone_at_position(position, level) or 0
        return 0

    def is_position_at_active_plex_or_lot(self, position, level):
        plex_service = services.get_plex_service()
        if plex_service.is_active_zone_a_plex():
            plex_zone_id_at_pick = plex_service.get_plex_zone_at_position(position, level)
            if plex_zone_id_at_pick is not None:
                if plex_zone_id_at_pick == services.current_zone_id():
                    return True
                return False
            return services.active_lot().is_position_on_lot(position)

    def is_position_at_active_plex(self, position, level):
        plex_service = services.get_plex_service()
        if plex_service.is_active_zone_a_plex():
            plex_zone_id_at_pick = plex_service.get_plex_zone_at_position(position, level)
            if plex_zone_id_at_pick is not None:
                if plex_zone_id_at_pick == services.current_zone_id():
                    return True
            return False

    def is_position_at_inactive_plex(self, position, level):
        plex_service = services.get_plex_service()
        if plex_service.is_active_zone_a_plex():
            plex_zone_id_at_pick = plex_service.get_plex_zone_at_position(position, level)
            if plex_zone_id_at_pick is not None:
                if plex_zone_id_at_pick != services.current_zone_id():
                    return True
            return False

    def get_all_zone_proto_buffs(self):
        return dict(((zone_proto.zone_id, zone_proto) for zone_proto in services.get_persistence_service().zone_proto_buffs_gen()))

    def is_zone_shutting_down(self):
        return services.current_zone().is_zone_shutting_down

    def is_position_outside(self, position, routing_surface_or_level):
        return _buildbuy.is_location_outside(services.current_zone_id(), position, routing_surface_or_level if isinstance(routing_surface_or_level, int) else routing_surface_or_level.secondary_id)

    def is_location_outside(self, location):
        return _buildbuy.is_location_outside(services.current_zone_id(), location.transform.translation, location.level)

    def is_location_water(self, location):
        routing_location = routing.Location(location.transform.translation, smath.Quaternion.IDENTITY(), location.routing_surface)
        if routing_location.routing_surface.type == routing.SurfaceType.SURFACETYPE_POOL or build_buy.is_location_pool(location.transform.translation, location.level):
            return True
        if terrain.get_water_depth_at_location(routing_location) > 0:
            return True
        return False

    def get_spawn_locations_gen(self, tags=None):
        for spawn_point in services.current_zone().spawn_points_gen():
            if tags:
                if set(spawn_point.get_tags()).intersection(set(tags)):
                    yield Location((spawn_point.get_approximate_center()), 0, 0, surface_override=(spawn_point.routing_surface))

    def get_spawn_position(self):
        spawn_point = services.current_zone().get_spawn_point()
        if spawn_point is not None:
            (trans, _) = spawn_point.next_spawn_spot()
            return trans
        return services.current_zone().lot.corners[1]

    def find_good_location_for_object(self, location, definition, **kwargs):
        if location is None or definition is None:
            return
        starting_location = placement.create_starting_location(position=(location.transform.translation), routing_surface=(location.routing_surface))
        fgl_context = (placement.create_fgl_context_for_object)(starting_location, definition, **kwargs)
        (trans, orient, _) = fgl_context.find_good_location()
        if trans is not None:
            if orient is not None:
                return location.clone(transform=(smath.Transform(trans, orient)))

    def find_good_location_for_sim(self, location, sim_instance, **kwargs):
        if location is None or sim_instance is None:
            return
        starting_location = placement.create_starting_location(location=location)
        fgl_context = (placement.create_fgl_context_for_sim)(starting_location, sim_instance, additional_avoid_sim_radius=routing.get_default_agent_radius(), **kwargs)
        (trans, orient, _) = fgl_context.find_good_location()
        if trans is not None:
            if orient is not None:
                return location.clone(transform=(smath.Transform(trans, orient)))

    def find_good_location(self, location, fallback_to_original=True, **kwargs):
        if location is None:
            return
        starting_location = placement.create_starting_location(location=location)
        fgl_context = (placement.FindGoodLocationContext)(starting_location, **kwargs)
        (trans, _, __) = fgl_context.find_good_location()
        if trans is None:
            if fallback_to_original:
                return location
            return
        return location.clone(transform=(smath.Transform(trans, smath.Quaternion.IDENTITY())))

    def get_terrain_height_at(self, x, z):
        return services.terrain_service.terrain_object().get_height_at(x, z)

    def get_routing_surface_height_at(self, x, z, routing_surface):
        return services.terrain_service.terrain_object().get_routing_surface_height_at(x, z, routing_surface)

    def get_water_depth_at(self, x, z, routing_surface_or_level=0):
        return terrain.get_water_depth(x, z, level=(routing_surface_or_level if isinstance(routing_surface_or_level, int) else routing_surface_or_level.secondary_id))


class OmutsuLotService(OmutsuService):

    def get_current_lot(self):
        return services.active_lot()

    def get_current_lot_id(self):
        return services.active_lot_id() or -1

    def get_all_lot_proto_buffs(self):
        return dict(((lot_proto.lot_description_id, lot_proto) for lot_proto in services.get_persistence_service().get_lots_proto_buff_gen()))

    def get_lot_household_id(self):
        household_id = services.owning_household_id_of_active_lot()
        if household_id is not None:
            return household_id
        return 0

    def is_position_on_lot(self, position):
        return services.active_lot().is_position_on_lot(position)

    def get_spawn_position(self):
        zone = services.current_zone()
        spawn_point = zone.active_lot_arrival_spawn_point or zone.get_spawn_point(lot_id=(self.get_current_lot_id()))
        if spawn_point is not None:
            (trans, _) = spawn_point.next_spawn_spot()
            return trans
        return services.current_zone().lot.corners[1]

    def get_current_venue_type(self):
        return build_buy.get_current_venue(services.current_zone_id())

    def set_current_venue_type(self, venue_type_id):
        venue_type = services.venue_manager().get(venue_type_id, None)
        if venue_type is not None:
            try:
                services.current_zone().venue_service.on_change_venue_type_at_runtime(venue_type)
            except:
                services.current_zone().venue_service.change_venue_type_at_runtime(venue_type)

    def is_venue_residential(self):
        venue_instance = get_resource_service().get_instance(OmutsuResourceType.VENUE, int(self.get_current_venue_type()))
        if venue_instance is not None:
            return venue_instance.residential
        return False

    def does_venue_require_player_greeting(self):
        venue_instance = get_resource_service().get_instance(OmutsuResourceType.VENUE, int(self.get_current_venue_type()))
        if venue_instance is not None:
            return venue_instance.requires_visitation_rights
        return False

    def does_venue_allow_routing_with_any_role_state(self):
        venue_instance = get_resource_service().get_instance(OmutsuResourceType.VENUE, int(self.get_current_venue_type()))
        if venue_instance is not None:
            return venue_instance.allow_rolestate_routing_on_navmesh
        return False

    def get_venue_type_display_name(self, venue_type_id):
        venue_instance = get_resource_service().get_instance(OmutsuResourceType.VENUE, venue_type_id)
        if venue_instance is not None:
            return venue_instance.display_name
        return get_l18n_service().get_localized_string(0)

    def has_lot_trait(self, *lot_trait_ids):
        zone_lot_trait_ids = {lot_trait.guid64 for lot_trait in services.get_zone_modifier_service().get_zone_modifiers(services.current_zone_id())}
        return not set(lot_trait_ids).isdisjoint(zone_lot_trait_ids)

    def get_block_dynamic_area_type(self, block_id):
        return services.dynamic_area_service().get_area_type_for_block(block_id)

    def get_object_dynamic_area_type(self, object_id):
        return services.dynamic_area_service().get_area_type_for_object(object_id)

    def get_room_id(self, position, routing_surface_or_level):
        return _buildbuy.get_room_id(services.current_zone_id(), position, routing_surface_or_level if isinstance(routing_surface_or_level, int) else routing_surface_or_level.secondary_id)

    def get_block_id(self, position, routing_surface_or_level):
        return _buildbuy.get_block_id(services.current_zone_id(), position, routing_surface_or_level if isinstance(routing_surface_or_level, int) else routing_surface_or_level.secondary_id)

    def get_all_blocks_ids(self, plex_id=None):
        return tuple(_buildbuy.get_all_block_polygons(services.current_zone_id(), plex_id if plex_id is not None else services.get_plex_service().get_active_zone_plex_id() or 0).keys())

    def get_all_blocks_polygons(self, plex_id=None):
        return _buildbuy.get_all_block_polygons(services.current_zone_id(), plex_id if plex_id is not None else services.get_plex_service().get_active_zone_plex_id() or 0)

    def get_lot_angle(self):
        return convert_orientation_to_angle(services.active_lot().orientation)

    def get_lot_corners(self):
        return list(services.active_lot().corners)


_WORLD_SERVICE = OmutsuWorldService("world")
_ZONE_SERVICE = OmutsuZoneService("zone")
_LOT_SERVICE = OmutsuLotService("lot")

def get_world_service() -> OmutsuWorldService:
    return _WORLD_SERVICE


def get_zone_service() -> OmutsuZoneService:
    return _ZONE_SERVICE


def get_lot_service() -> OmutsuLotService:
    return _LOT_SERVICE
