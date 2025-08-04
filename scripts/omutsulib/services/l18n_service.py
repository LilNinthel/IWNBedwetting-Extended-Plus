from protocolbuffers.Localization_pb2 import LocalizedString
from sims4.localization import LocalizationHelperTuning, _create_localized_string, create_tokens, TunableLocalizedStringFactory
from omutsulib.services.service import OmutsuService

class OmutsuLocalizedListType:
    NONE = 0
    SPACE = 1
    NEW_LINE = 2
    DOUBLE_NEW_LINE = 3
    BULLET = 4
    COMMA = 5


LOCALIZED_LIST_TYPES = {(OmutsuLocalizedListType.NONE): (3022309381, 2718603618), 
 (OmutsuLocalizedListType.SPACE): (3022309381, 1568702465), 
 (OmutsuLocalizedListType.NEW_LINE): (3022309381, 288320353), 
 (OmutsuLocalizedListType.DOUBLE_NEW_LINE): (3022309381, 1097768731), 
 (OmutsuLocalizedListType.BULLET): (3638435065, 3489403491), 
 (OmutsuLocalizedListType.COMMA): (3022309381, 1085256118)}

class OmutsuL18NService(OmutsuService):

    def get_localized_string(self, object_value, tokens=(), raw_tokens=False):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        if object_value is None:
            return self.get_localized_string(0)
        verified_tokens = [self.get_localized_string(token) for token in tokens] if (not raw_tokens) else tokens
        if isinstance(object_value, LocalizedString):
            create_tokens(object_value.tokens, verified_tokens)
            return object_value
        if isinstance(object_value, TunableLocalizedStringFactory._Wrapper):
            return self.get_localized_string_from_stbl_id((object_value._string_id), tokens=verified_tokens)
        if isinstance(object_value, int):
            return self.get_localized_string_from_stbl_id(object_value, tokens=verified_tokens)
        if isinstance(object_value, str):
            return self.get_localized_string((self.get_localized_string_from_text(object_value)), tokens=verified_tokens)
        if hasattr(object_value, "populate_localization_token"):
            return object_value
        if isinstance(object_value, OmutsuSim):
            return object_value.get_sim_info()
        return self.get_localized_string((str(object_value)), tokens=verified_tokens)

    def create_localized_list(self, list_type, entries):
        global LOCALIZED_LIST_TYPES
        (list_base, list_entry) = LOCALIZED_LIST_TYPES[list_type]
        localized_string_entries = None
        for localized_entry in entries:
            if localized_string_entries is None:
                localized_string_entries = get_l18n_service().get_localized_string(list_base, tokens=(localized_entry,))
            else:
                localized_string_entries = get_l18n_service().get_localized_string(list_entry, tokens=(localized_string_entries, localized_entry))

        return localized_string_entries

    def create_localized_string_list(self, string_base, string_entries):
        localized_string_entries = None
        for string_entry in string_entries:
            if localized_string_entries is None:
                localized_string_entries = get_l18n_service().get_localized_string(string_entry)
            else:
                localized_string_entries = get_l18n_service().get_localized_string(string_base, tokens=(localized_string_entries, string_entry))

        return localized_string_entries

    def get_localized_string_from_text(self, text):
        return LocalizationHelperTuning.get_raw_text(text)

    def get_localized_string_from_stbl_id(self, text_id, tokens=()):
        return _create_localized_string(text_id, *tokens)

    def get_localized_string_id(self, localized_string):
        return localized_string.hash


_L18N_SERVICE = OmutsuL18NService("l18n")

def get_l18n_service() -> OmutsuL18NService:
    return _L18N_SERVICE
