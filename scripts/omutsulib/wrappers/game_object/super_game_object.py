import weakref, services
from objects.game_object import GameObject
from omutsulib.services.persistence_service import get_persistence_service
from omutsulib.services.world_service import get_world_service, get_zone_service
from omutsulib.utils.cacher import cache_return
from omutsulib.wrappers.wrappers_manager import OmutsuInstance, OmutsuInstanceSingleton
_super_game_object_persistence_key_cache = None

def _update_persistence_key(from_load=False, **_):
    global _super_game_object_persistence_key_cache
    if from_load:
        _super_game_object_persistence_key_cache = OmutsuGameObjectSingleton.create_persistence_key()


get_persistence_service().register_save_slot_id_update_callback(_update_persistence_key)

class OmutsuGameObjectSingleton(OmutsuInstanceSingleton):
    _is_persistent = True

    def get_key(cls, object_instance, *args, **kwargs):
        object_id = _get_game_object_instance_id(object_instance)
        if object_id is not None:
            return (object_id, cls.__name__)

    @staticmethod
    def create_persistence_key():
        return (
         get_persistence_service().get_save_slot_guid(), get_persistence_service().get_save_slot_id(), get_world_service().get_current_world_id(), get_zone_service().get_current_zone_id())

    def get_persistence_key(cls):
        global _super_game_object_persistence_key_cache
        if _super_game_object_persistence_key_cache is None:
            _super_game_object_persistence_key_cache = cls.create_persistence_key()
        return _super_game_object_persistence_key_cache


class _SuperOmutsuGameObject(OmutsuInstance):

    def __init__(self, *args, proxy_object=False):
        game_object_identifier = args[0]
        self._object_id = _get_game_object_instance_id(game_object_identifier, proxy_object=proxy_object)
        self._object_instance = weakref.ref(game_object_identifier) if (game_object_identifier.__class__ is GameObject or proxy_object) else None
        self._unique_id = None
        super().__init__(self._object_id)
        self._temp_values = {}

    def __new__(cls, *args, proxy_object=False):
        game_object_identifier = args[0]
        if isinstance(game_object_identifier, _SuperOmutsuGameObject):
            return game_object_identifier
        if not proxy_object:
            if _get_game_object_instance_id(game_object_identifier) is None:
                return
        return super().__new__(cls)

    def get_object_id(self):
        return self._object_id

    def get_object_guid(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return getattr(object_instance, "guid64", 0)
        return 0

    def get_object_instance(self):
        if self._object_instance is not None:
            object_instance = self._object_instance()
            if object_instance is not None:
                return object_instance
        object_instance = services.object_manager().get(self._object_id) or services.inventory_manager().get(self._object_id)
        if object_instance is None:
            return
        self._object_instance = weakref.ref(object_instance)
        return object_instance

    def get_object_definition(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.definition

    def get_object_definition_id(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.definition.id
        return 0

    def get_household_owner_id(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.get_household_owner_id()
        return 0

    def set_household_owner_id(self, household_id):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            object_instance.set_household_owner_id(household_id)

    def get_unique_id(self):
        if self._unique_id is None:
            self._unique_id = self._get_unique_id()
        return self._unique_id

    def _get_unique_id(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return _get_object_inorganic_unique_id(int(getattr(object_instance, "guid64", 0)), int(getattr(object_instance, "catalog_name", 0)))
        return -1

    def get_temp_value(self, key, default=None):
        if isinstance(default, type) and issubclass(default, (dict, list, set)):
            if key not in self._temp_values:
                self._temp_values[key] = default()
            return self._temp_values.get(key, default)

    def set_temp_value(self, key, value):
        self._temp_values[key] = value

    def remove_temp_value(self, key):
        self._temp_values.pop(key, None)


def _get_game_object_instance_id(game_object_identifier, proxy_object=False):
    if proxy_object:
        return
    if game_object_identifier is None:
        return
    if isinstance(game_object_identifier, _SuperOmutsuGameObject):
        return game_object_identifier.get_object_id()
    if isinstance(game_object_identifier, GameObject):
        return getattr(game_object_identifier, "id", None)
    if isinstance(game_object_identifier, int):
        object_instance = services.object_manager().get(game_object_identifier) or services.inventory_manager().get(game_object_identifier)
        if object_instance is not None:
            return getattr(object_instance, "id", None)


@cache_return(cache_max_size=5000)
def _get_object_inorganic_unique_id(guid64, catalog_name):
    if guid64 > catalog_name:
        identifier_data = [
         int(catalog_name), int(guid64)]
    else:
        identifier_data = [
         int(guid64), int(catalog_name)]
    hash_value = 3430008
    for item in identifier_data:
        hash_value = eval(hex(1000003 * hash_value & 4294967295)[:-1]) ^ item

    hash_value ^= len(identifier_data)
    return abs(hash_value)
