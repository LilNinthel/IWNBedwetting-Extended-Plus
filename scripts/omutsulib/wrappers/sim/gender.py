from typing import TYPE_CHECKING
from omutsulib.native_enums.traits import NativeTrait
from omutsulib.services.components_service import get_components_service, OmutsuComponentType
from omutsulib.wrappers.enum import OmutsuIntEnum
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required
if TYPE_CHECKING:
    from omutsulib.wrappers.sim.sim import OmutsuSim

class OmutsuGender(OmutsuIntEnum):
    MALE = 4096
    FEMALE = 8192
    NONBINARY = 16384


class OmutsuGenderPreferenceType(OmutsuIntEnum):
    ROMANTIC = 1
    WOOHOO = 2


class OmutsuGenderPreferenceAttraction(OmutsuIntEnum):
    NOT_ATTRACTED = 0
    ATTRACTED = 1


GENDER_PREFERENCES_ATTRACTION_MAP = {(OmutsuGenderPreferenceType.ROMANTIC): {(OmutsuGender.MALE): {(OmutsuGenderPreferenceAttraction.ATTRACTED): (NativeTrait.GENDER_OPTIONS_ATTRACTED_TO_MALE), 
                                                             (OmutsuGenderPreferenceAttraction.NOT_ATTRACTED): (NativeTrait.GENDER_OPTIONS_ATTRACTED_TO_NOT_MALE)}, 
                                        
                                        (OmutsuGender.FEMALE): {(OmutsuGenderPreferenceAttraction.ATTRACTED): (NativeTrait.GENDER_OPTIONS_ATTRACTED_TO_FEMALE), 
                                                               (OmutsuGenderPreferenceAttraction.NOT_ATTRACTED): (NativeTrait.GENDER_OPTIONS_ATTRACTED_TO_NOT_FEMALE)}, 
                                        
                                        (OmutsuGender.NONBINARY): {(OmutsuGenderPreferenceAttraction.ATTRACTED): 0, 
                                                                  (OmutsuGenderPreferenceAttraction.NOT_ATTRACTED): 0}}, 
 
 (OmutsuGenderPreferenceType.WOOHOO): {(OmutsuGender.MALE): {(OmutsuGenderPreferenceAttraction.ATTRACTED): (NativeTrait.SEXUAL_ORIENTATION_WOO_HOO_INTERESTS_MALE), 
                                                           (OmutsuGenderPreferenceAttraction.NOT_ATTRACTED): (NativeTrait.SEXUAL_ORIENTATION_WOO_HOO_INTERESTS_NOT_MALE)}, 
                                      
                                      (OmutsuGender.FEMALE): {(OmutsuGenderPreferenceAttraction.ATTRACTED): (NativeTrait.SEXUAL_ORIENTATION_WOO_HOO_INTERESTS_FEMALE), 
                                                             (OmutsuGenderPreferenceAttraction.NOT_ATTRACTED): (NativeTrait.SEXUAL_ORIENTATION_WOO_HOO_INTERESTS_NOT_FEMALE)}, 
                                      
                                      (OmutsuGender.NONBINARY): {(OmutsuGenderPreferenceAttraction.ATTRACTED): 0, 
                                                                (OmutsuGenderPreferenceAttraction.NOT_ATTRACTED): 0}}}

class _OmutsuSimGenderMixin(_SuperOmutsuSim):

    @sim_info_required(default=0, base_wrapper=True)
    def get_gender(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return sim_info.gender

    @sim_info_required(base_wrapper=True)
    def set_gender(self, gender):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info.gender = gender

    @sim_info_required()
    def set_gender_preference(self: "OmutsuSim", gender, is_attracted, gender_preference_type=OmutsuGenderPreferenceType.ROMANTIC):
        if gender_preference_type == OmutsuGenderPreferenceType.ROMANTIC:
            self.set_gender_preference_value(gender, 100.0 if is_attracted else 0.0)
        preference_type_map = GENDER_PREFERENCES_ATTRACTION_MAP[gender_preference_type]
        preference_genders_map = preference_type_map[gender]
        if is_attracted:
            self.add_trait(preference_genders_map[OmutsuGenderPreferenceAttraction.ATTRACTED])
            self.remove_trait(preference_genders_map[OmutsuGenderPreferenceAttraction.NOT_ATTRACTED])
        else:
            self.add_trait(preference_genders_map[OmutsuGenderPreferenceAttraction.NOT_ATTRACTED])
            self.remove_trait(preference_genders_map[OmutsuGenderPreferenceAttraction.ATTRACTED])

    @sim_info_required()
    def get_gender_preference(self: "OmutsuSim", gender, gender_preference_type=OmutsuGenderPreferenceType.ROMANTIC):
        preference_type_map = GENDER_PREFERENCES_ATTRACTION_MAP[gender_preference_type]
        preference_genders_map = preference_type_map[gender]
        if self.has_trait(preference_genders_map[OmutsuGenderPreferenceAttraction.ATTRACTED]):
            return True
        return False

    @sim_info_required()
    def is_gender_preference_exploring(self: "OmutsuSim"):
        sim_info = self.get_sim_info()
        return sim_info.is_exploring_sexuality

    @sim_info_required()
    def set_gender_preference_value(self, gender, value):
        if get_components_service().has_object_component(self.get_sim_info(), OmutsuComponentType.STATISTIC):
            gender_preference = self.get_sim_info().get_gender_preference(gender)
            if gender_preference is not None:
                gender_preference.set_value(value)

    @sim_info_required(default=0)
    def get_gender_preference_value(self, gender):
        if get_components_service().has_object_component(self.get_sim_info(), OmutsuComponentType.STATISTIC):
            gender_preference = self.get_sim_info().get_gender_preference(gender)
            if gender_preference is not None:
                return gender_preference.get_value()
            return 0
