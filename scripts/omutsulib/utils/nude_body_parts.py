from omutsulib.services.cas_service import OmutsuBodyType
from omutsulib.wrappers.sim.age import OmutsuAge
from omutsulib.wrappers.sim.gender import OmutsuGender
from omutsulib.wrappers.sim.occult import OmutsuOccultType
from omutsulib.wrappers.sim.sim import OmutsuSim


def get_sim_default_nude_cas_part_id(omutsu_sim: OmutsuSim, body_type):
    return get_default_nude_cas_part_id((omutsu_sim.get_gender()), body_type, occult_type=(omutsu_sim.get_current_occult_type()), age=omutsu_sim.get_age())


def get_default_nude_cas_part_id(gender, body_type, occult_type=None, age=OmutsuAge.NONE):
    if age in (OmutsuAge.TEEN, OmutsuAge.YOUNGADULT, OmutsuAge.ADULT, OmutsuAge.ELDER):
        if occult_type == OmutsuOccultType.WEREWOLF:
            if gender == OmutsuGender.MALE:
                if body_type == OmutsuBodyType.UPPER_BODY:
                    return 314304
                if body_type == OmutsuBodyType.LOWER_BODY:
                    return 313811
                if body_type == OmutsuBodyType.SHOES:
                    return 313823
            if gender == OmutsuGender.FEMALE:
                if body_type == OmutsuBodyType.UPPER_BODY:
                    return 313825
                if body_type == OmutsuBodyType.LOWER_BODY:
                    return 313809
                if body_type == OmutsuBodyType.SHOES:
                    return 313815
        else:
            if gender == OmutsuGender.MALE:
                if body_type == OmutsuBodyType.UPPER_BODY:
                    return 6562
                if body_type == OmutsuBodyType.LOWER_BODY:
                    return 6574
                if body_type == OmutsuBodyType.SHOES:
                    return 6563
            if gender == OmutsuGender.FEMALE:
                if body_type == OmutsuBodyType.UPPER_BODY:
                    return 6540
                if body_type == OmutsuBodyType.LOWER_BODY:
                    return 6544
                if body_type == OmutsuBodyType.SHOES:
                    return 6543
    elif age == OmutsuAge.CHILD:
        if body_type == OmutsuBodyType.UPPER_BODY:
            if gender == OmutsuGender.FEMALE:
                return 350495
            elif gender == OmutsuGender.MALE:
                return 22069
        if body_type == OmutsuBodyType.LOWER_BODY:
            return 22074
        if body_type == OmutsuBodyType.SHOES:
            return 22018
    return -1
