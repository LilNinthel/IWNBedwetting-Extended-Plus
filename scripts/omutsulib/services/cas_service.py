from buffs.appearance_modifier.appearance_modifier import AppearanceModifier
from cas.cas import get_caspart_bodytype, get_buff_from_part_ids
from sims.outfits.outfit_enums import BodyType, OutfitCategory, CLOTHING_BODY_TYPES, BodyTypeFlag
from sims.outfits.outfit_utils import get_maximum_outfits_for_category
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims4.repr_utils import standard_repr
from omutsulib.services.service import OmutsuService
from omutsulib.wrappers.enum import OmutsuIntEnum, OmutsuIntFlagsEnum
NO_COLOR_SHIFT = 4611686018427387904

class OmutsuOutfitCategory(OmutsuIntEnum):
    CURRENT_OUTFIT = -1
    EVERYDAY = 0
    FORMAL = 1
    ATHLETIC = 2
    SLEEP = 3
    PARTY = 4
    BATHING = 5
    CAREER = 6
    SITUATION = 7
    SPECIAL = 8
    SWIMWEAR = 9
    HOT_WEATHER = 10
    COLD_WEATHER = 11
    BATUU = 12
    SMALL_BUSINESS = 13

    @staticmethod
    def get_outfit_category(outfit_category_id):
        return OutfitCategory(int(outfit_category_id))

    @staticmethod
    def get_maximum_outfits_for_outfit_category(outfit_category):
        return get_maximum_outfits_for_category(outfit_category)


CAS_OUTFIT_CATEGORIES = (
 OmutsuOutfitCategory.EVERYDAY, OmutsuOutfitCategory.FORMAL, OmutsuOutfitCategory.ATHLETIC, OmutsuOutfitCategory.SLEEP, OmutsuOutfitCategory.PARTY, OmutsuOutfitCategory.SWIMWEAR, OmutsuOutfitCategory.HOT_WEATHER, OmutsuOutfitCategory.COLD_WEATHER)

class SimOutfitChangeReason:
    Invalid = -1
    PreviousClothing = 0
    DefaultOutfit = 1
    RandomOutfit = 2
    ExitBedNPC = 3
    CurrentOutfit = 4
    FashionOutfit = 5
    EnterBathing = 6
    Category_Party = 7
    ExitShower = 8
    Category_Sleep = 9
    GoToWork = 10
    Category_Athletic = 11
    Situation = 12
    Category_Formal = 13
    Category_Everyday = 14
    EnterBedWooHoo = 15
    Current_Outfit = 16
    Category_Swimwear = 17
    ExitPool = 18
    ExitWorkout = 19
    NPCLeavingActiveLot = 20
    ExitHotTub = 21
    EnterHotTub = 22
    Category_Yoga_Enter = 23
    Category_Yoga_Exit = 24
    ExitNude = 25
    EnterDying = 26
    EnterToddlerInfantBathing = 27
    ExitToddlerInfantBathing = 28
    EnterPetBathing = 29
    Category_ColdWeather = 30
    Category_HotWeather = 31
    WeatherBased = 32
    EnterToddlerSwimming = 33
    EnterHotSprings = 34
    ExitToddlerSwimming = 35
    EnterSunbatheSwimwear = 36
    EnterOceanWater = 37
    ExitHotSprings = 38
    RockClimbing = 39
    GoToSchool = 40
    SmallBusinessWork = 41


class OmutsuBodyType(OmutsuIntEnum):
    NONE = 0
    HAT = 1
    HAIR = 2
    HEAD = 3
    TEETH = 4
    FULL_BODY = 5
    UPPER_BODY = 6
    LOWER_BODY = 7
    SHOES = 8
    CUMMERBUND = 9
    EARRINGS = 10
    GLASSES = 11
    NECKLACE = 12
    GLOVES = 13
    WRIST_LEFT = 14
    WRIST_RIGHT = 15
    LIP_RING_LEFT = 16
    LIP_RING_RIGHT = 17
    NOSE_RING_LEFT = 18
    NOSE_RING_RIGHT = 19
    BROW_RING_LEFT = 20
    BROW_RING_RIGHT = 21
    INDEX_FINGER_LEFT = 22
    INDEX_FINGER_RIGHT = 23
    RING_FINGER_LEFT = 24
    RING_FINGER_RIGHT = 25
    MIDDLE_FINGER_LEFT = 26
    MIDDLE_FINGER_RIGHT = 27
    FACIAL_HAIR = 28
    LIPS_TICK = 29
    EYE_SHADOW = 30
    EYE_LINER = 31
    BLUSH = 32
    FACE_PAINT = 33
    EYEBROWS = 34
    EYE_COLOR = 35
    SOCKS = 36
    EYELASHES = 37
    SKIN_DETAIL_CREASE_FOREHEAD = 38
    SKIN_DETAIL_FRECKLES = 39
    SKIN_DETAIL_DIMPLE_LEFT = 40
    SKIN_DETAIL_DIMPLE_RIGHT = 41
    TIGHTS = 42
    SKIN_DETAIL_MOLE_LIP_LEFT = 43
    SKIN_DETAIL_MOLE_LIP_RIGHT = 44
    TATTOO_ARM_LOWER_LEFT = 45
    TATTOO_ARM_UPPER_LEFT = 46
    TATTOO_ARM_LOWER_RIGHT = 47
    TATTOO_ARM_UPPER_RIGHT = 48
    TATTOO_LEG_LEFT = 49
    TATTOO_LEG_RIGHT = 50
    TATTOO_TORSO_BACK_LOWER = 51
    TATTOO_TORSO_BACK_UPPER = 52
    TATTOO_TORSO_FRONT_LOWER = 53
    TATTOO_TORSO_FRONT_UPPER = 54
    SKIN_DETAIL_MOLE_CHEEK_LEFT = 55
    SKIN_DETAIL_MOLE_CHEEK_RIGHT = 56
    SKIN_DETAIL_CREASE_MOUTH = 57
    SKIN_OVERLAY = 58
    FUR_BODY = 59
    EARS = 60
    TAIL = 61
    SKIN_DETAIL_NOSE_COLOR = 62
    EYE_COLOR_SECONDARY = 63
    OCCULT_BROW = 64
    OCCULT_EYE_SOCKET = 65
    OCCULT_EYE_LID = 66
    OCCULT_MOUTH = 67
    OCCULT_LEFT_CHEEK = 68
    OCCULT_RIGHT_CHEEK = 69
    OCCULT_NECK_SCAR = 70
    FOREARM_SCAR = 71
    ACNE = 72
    FINGERNAIL = 73
    TOENAIL = 74
    HAIRCOLOR_OVERRIDE = 75
    BITE = 76
    BODYFRECKLES = 77
    BODYHAIR_ARM = 78
    BODYHAIR_LEG = 79
    BODYHAIR_TORSOFRONT = 80
    BODYHAIR_TORSOBACK = 81
    BODYSCAR_ARMLEFT = 82
    BODYSCAR_ARMRIGHT = 83
    BODYSCAR_TORSOFRONT = 84
    BODYSCAR_TORSOBACK = 85
    BODYSCAR_LEGLEFT = 86
    BODYSCAR_LEGRIGHT = 87
    ATTACHMENT_BACK = 88
    SKINDETAIL_ACNE_PUBERTY = 89
    SCARFACE = 90
    BIRTHMARKFACE = 91
    BIRTHMARKTORSOBACK = 92
    BIRTHMARKTORSOFRONT = 93
    BIRTHMARKARMS = 94
    MOLEFACE = 95
    MOLECHESTUPPER = 96
    MOLEBACKUPPER = 97
    BIRTHMARKLEGS = 98
    STRETCHMARKS_FRONT = 99
    STRETCHMARKS_BACK = 100
    SADDLE = 101
    BRIDLE = 102
    REINS = 103
    BLANKET = 104
    SKINDETAIL_HOOF_COLOR = 105
    HAIR_MANE = 106
    HAIR_TAIL = 107
    HAIR_FORELOCK = 108
    HAIR_FEATHERS = 109
    HORN = 110
    TAIL_BASE = 111
    BIRTHMARKOCCULT = 112
    TATTOO_HEAD = 113
    WINGS = 114
    HEADDECO = 115
    SKINSPECULARITY = 116
    UNUSED = 117

    @staticmethod
    def get_all_non_clothing_body_types():
        return [body_type for body_type in BodyType if body_type not in CLOTHING_BODY_TYPES]


class OmutsuCasPart:

    def __init__(self, cas_part, color_shift=NO_COLOR_SHIFT, object_id=0, layer_id=0):
        self.cas_part = cas_part
        self.color_shift = color_shift
        self.object_id = object_id
        self.layer_id = layer_id

    def __int__(self):
        return self.cas_part

    def __eq__(self, other):
        return self.cas_part == other.cas_part and self.color_shift == other.color_shift and self.object_id == other.object_id and self.layer_id == other.layer_id

    def __hash__(self):
        return hash((self.cas_part, self.color_shift, self.object_id, self.layer_id))

    def __repr__(self):
        return "OmutsuCasPart({}, color_shift={}, object_id={}, layer_id={})".format(self.cas_part, self.color_shift, self.object_id, self.layer_id)


EMPTY_CAS_PART = OmutsuCasPart(0)

class OmutsuAppearanceModifierType:
    SET_CAS_PART = 0
    RANDOMIZE_BODY_TYPE_COLOR = 1
    RANDOMIZE_SKINTONE_FROM_TAGS = 2
    GENERATE_OUTFIT = 3
    RANDOMIZE_CAS_PART = 4
    SET_ATTACHMENT = 5
    REMOVE_CAS_PART = 6
    EMOVE_CAS_PART_BY_BODY_TYPE = 7
    MERGING = 10


class OmutsuAppearanceModifierPriority(OmutsuIntEnum):
    INVALID = 0
    MANNEQUIN = 1
    SICKNESS = 2
    PATIENT = 3
    TRANSFORMED = 4
    FROZEN = 5


class OmutsuOutfitOverrideOptionFlag(OmutsuIntFlagsEnum):
    DEFAULT = 0
    OVERRIDE_ALL_OUTFITS = 1
    IGNORE_BATHING = 2
    MANNEQUIN_MODE = 4
    APPLY_MODIFIER_VARIATION = 8
    FROM_SCRATCH = 16
    APPLY_GENETICS_FROM_OVERRIDE = 32
    OVERRIDE_CUSTOM_TEXTURES = 64
    OVERRIDE_HAIR_MATCH_FLAGS = 128
    OVERRIDE_SKIP_UI_CHECKS = 256
    SKIP_BODY_MODIFICATIONS = 512


class OmutsuMergingAppearanceModifierSource(OmutsuIntEnum):
    UNKNOWN = 0


class MergingAppearanceModifier(AppearanceModifier.BaseAppearanceModification):

    def __init__(self, owner_omutsu_sim, outfit_parts, modifier_source=OmutsuMergingAppearanceModifierSource.UNKNOWN, is_permanent=False, appearance_modifier_tag=None, should_refresh_thumbnail=False):
        super().__init__(_is_combinable_with_same_type=True, outfit_type_compatibility=None, appearance_modifier_tag=appearance_modifier_tag, should_refresh_thumbnail=should_refresh_thumbnail)
        self.owner_omutsu_sim = owner_omutsu_sim
        self.override_outfit_parts = outfit_parts
        self.modifier_source = modifier_source
        self.is_permanent = is_permanent

    def modify_sim_info(self, source_sim_info, modified_sim_info, random_seed):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        SimInfoBaseWrapper.copy_base_attributes(modified_sim_info, source_sim_info)
        SimInfoBaseWrapper.copy_physical_attributes(modified_sim_info, source_sim_info)
        modified_sim_info.skin_tone = source_sim_info._base.skin_tone
        modified_sim_info.skin_tone_val_shift = source_sim_info._base.skin_tone_val_shift
        modified_sim_info.load_outfits(source_sim_info.save_outfits())
        source_omutsu_sim = OmutsuSim(source_sim_info, exclusive_base_wrapper=True)
        modified_omutsu_sim = OmutsuSim(modified_sim_info, exclusive_base_wrapper=True)
        outfit_category_and_index = self.owner_omutsu_sim.get_current_outfit()
        if source_omutsu_sim.has_outfit(outfit_category_and_index):
            if modified_omutsu_sim.has_outfit(outfit_category_and_index):
                outfit_parts = dict(source_omutsu_sim.get_outfit_parts(outfit_category_and_index))
                outfit_parts.update(self.override_outfit_parts)
                modified_omutsu_sim.set_outfit_parts(outfit_category_and_index, outfit_parts)
            return (
             (BodyTypeFlag.make_body_type_flag)(*self.override_outfit_parts.keys()), None)

    def get_modifier_source(self):
        return self.modifier_source

    @property
    def is_permanent_modification(self):
        return self.is_permanent

    @property
    def modifier_type(self):
        return OmutsuAppearanceModifierType.MERGING

    @property
    def combinable_sorting_key(self):
        return next(iter(self.override_outfit_parts))

    def __repr__(self):
        return standard_repr(self, outfit_parts=(self.override_outfit_parts), is_permanent=(self.is_permanent))


class OmutsuCASService(OmutsuService):

    def is_cas_part_loaded(self, cas_part_id):
        return get_caspart_bodytype(int(cas_part_id)) > 0

    def get_cas_part_body_type_id(self, cas_part_id):
        return get_caspart_bodytype(int(cas_part_id))

    def get_cas_part_buff_id(self, cas_part_id):
        return int(get_buff_from_part_ids(int(cas_part_id)))


_CAS_SERVICE = OmutsuCASService("cas")

def get_cas_service() -> OmutsuCASService:
    return _CAS_SERVICE
