import collections, objects.system, services
from build_buy import get_object_catalog_name
from objects import MaterialState
from objects.terrain import TerrainPoint
from omutsulib.services.service import OmutsuService
from omutsulib.wrappers.game_object.game_object import OmutsuGameObject
from omutsulib.wrappers.game_object.super_game_object import _get_object_inorganic_unique_id

class OmutsuGameObjectsService(OmutsuService):

    def get_definition(self, object_guid, pack_safe=False, get_fallback_definition_id=True):
        return services.definition_manager().get(object_guid, pack_safe=pack_safe, get_fallback_definition_id=get_fallback_definition_id)

    def get_definition_footprint(self, definition, index=0):
        return definition.get_footprint(index=index)

    def create_game_object(self, object_definition, init=None, post_add=None, location=None, opacity=None, geometry_state=None, material_state=None, owner_household_id=-1):
        game_object = objects.system.create_object(object_definition, init=init, post_add=post_add)
        if game_object is not None:
            if location is not None:
                game_object.location = location
            if opacity is not None:
                game_object.opacity = opacity
            if geometry_state is not None:
                game_object.geometry_state = geometry_state
            if material_state is not None:
                game_object.material_state = MaterialState(material_state)
            if owner_household_id != -1:
                game_object.set_household_owner_id(owner_household_id)
            return game_object

    def get_all_omutsu_game_objects_gen(self, definitions=None, tags=None, valid=True, is_in_world=True, is_in_inventory=False):
        if valid:
            for game_object in services.object_manager().valid_objects():
                if game_object is None:
                    continue
                if is_in_world:
                    if not game_object.is_in_inventory():
                        if game_object.routing_surface is None:
                            continue
                if is_in_inventory:
                    if not game_object.is_in_inventory():
                        continue
                if definitions:
                    if game_object.definition.id not in definitions:
                        continue
                if tags:
                    if not game_object.get_tags() & tags:
                        continue
                yield OmutsuGameObject(game_object)

        else:
            for game_object in services.object_manager().get_all():
                if game_object is None:
                    continue
                if is_in_world:
                    if not game_object.is_in_inventory():
                        if game_object.routing_surface is None:
                            continue
                if is_in_inventory:
                    if not game_object.is_in_inventory():
                        continue
                if definitions:
                    if game_object.definition.id not in definitions:
                        continue
                if tags:
                    if not game_object.get_tags() & tags:
                        continue
                yield OmutsuGameObject(game_object)

    def create_terrain_point(self, location):
        return TerrainPoint(location)

    def get_all_unique_ids_to_definition_cls(self):
        tuning_guid_to_def_ids = collections.defaultdict(set)
        for (def_id, definition) in services.definition_manager()._definitions_cache.items():
            tuning_guid_to_def_ids[definition.cls.guid64].add(def_id)

        uid_to_def_cls = {}
        for (tuning_guid, def_ids) in tuning_guid_to_def_ids.items():
            for def_id in def_ids:
                if isinstance(def_id, tuple):
                    def_id = def_id[0]
                try:
                    catalog_name = get_object_catalog_name(def_id)
                except:
                    catalog_name = 0

                uid = _get_object_inorganic_unique_id(tuning_guid, catalog_name)
                definition = services.definition_manager().get(def_id)
                if definition is not None:
                    uid_to_def_cls[uid] = definition.cls

        return uid_to_def_cls

    def get_all_unique_ids_to_definition_ids(self):
        tuning_guid_to_def_ids = collections.defaultdict(set)
        for (def_id, definition) in services.definition_manager()._definitions_cache.items():
            tuning_guid_to_def_ids[definition.cls.guid64].add(def_id)

        uid_to_def_ids = {}
        for (tuning_guid, def_ids) in tuning_guid_to_def_ids.items():
            for def_id in def_ids:
                if isinstance(def_id, tuple):
                    def_id = def_id[0]
                try:
                    catalog_name = get_object_catalog_name(def_id)
                except:
                    catalog_name = 0

                uid = _get_object_inorganic_unique_id(tuning_guid, catalog_name)
                uid_to_def_ids[uid] = def_id

        return uid_to_def_ids


_GAME_OBJECTS_SERVICE = OmutsuGameObjectsService("game_objects")

def get_game_objects_service() -> OmutsuGameObjectsService:
    return _GAME_OBJECTS_SERVICE
