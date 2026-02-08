import services
from services.persistence_service import PersistenceService, SaveGameData
from omutsulib.services.service import OmutsuService
from omutsulib.utils.injector import inject
from zone import Zone
_current_real_save_slot = 0

class OmutsuPersistenceService(OmutsuService):

    def __init__(self, name):
        super().__init__(name)
        self.save_slot_id_update_callbacks = []

    def get_save_slot_name(self):
        save_game_data_proto = services.get_persistence_service()._save_game_data_proto
        if save_game_data_proto is not None:
            return save_game_data_proto.save_slot.slot_name
        return ""

    def get_save_slot_guid(self):
        return services.get_persistence_service().get_save_slot_proto_guid()

    def get_save_slot_id(self, native=False):
        global _current_real_save_slot
        if native:
            return services.get_persistence_service().get_save_slot_proto_buff().slot_id
        return _current_real_save_slot or services.get_persistence_service().get_save_slot_proto_buff().slot_id

    def _update_save_slot_id(self, from_load=False, from_save=False):
        global _current_real_save_slot
        slot_id = services.get_persistence_service().get_save_slot_proto_buff().slot_id
        if slot_id != 0:
            _current_real_save_slot = slot_id
        for callback_func in self.save_slot_id_update_callbacks:
            callback_func(from_load=from_load, from_save=from_save)

    def register_save_slot_id_update_callback(self, callback_func):
        self.save_slot_id_update_callbacks.append(callback_func)

    def save_game(self, save_slot_id, save_slot_name, force_override=False):
        persistence_service = services.get_persistence_service()
        if not persistence_service.is_save_locked():
            save_game_data = SaveGameData(save_slot_id, save_slot_name, force_override, None)
            persistence_service.save_using((persistence_service.save_game_gen), save_game_data, send_save_message=True, check_cooldown=False)
            return True
        return False


@inject(Zone, "load_zone")
def _iwnbedwetting_on_zone_load_update_slot_id(original, self, *args, **kwargs):
    try:
        get_persistence_service()._update_save_slot_id(from_load=True)
    except:
        pass

    try:
        result = original(self, *args, **kwargs)
    except:
        result = None

    try:
        get_persistence_service()._update_save_slot_id(from_load=True)
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to catch save slot id at '_iwnbedwetting_on_zone_load_update_slot_id' at 'Zone.load_zone'.", ex)
        finally:
            ex = None
            del ex

    return result


@inject(PersistenceService, "_destroy_save_timeline")
def _iwnbedwetting_on_save_finish_update_slot_id(original, self, *args, **kwargs):
    try:
        get_persistence_service()._update_save_slot_id(from_save=True)
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to catch save slot id at '_iwnbedwetting_on_save_finish_update_slot_id' at 'PersistenceService._destroy_save_timeline'.", ex)
        finally:
            ex = None
            del ex

    return original(self, *args, **kwargs)


_PERSISTENCE_SERVICE = OmutsuPersistenceService("persistence")

def get_persistence_service() -> OmutsuPersistenceService:
    return _PERSISTENCE_SERVICE
