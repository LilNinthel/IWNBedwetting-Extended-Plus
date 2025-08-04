import random
import traceback
import iwnbedwetting.main
import services

from iwnbedwetting.diaper_cas_part_config.snippet import DiaperLoadCASConfig
from omutsulib.enums.buffs import IwnBedwettingBuff
from omutsulib.enums.diapers import DiaperFrame, DiaperCC, DiaperHeight, DiaperBodyType
from omutsulib.enums.statistics import IwnBedwettingStatistic
from omutsulib.enums.traits import IwnBedwettingTrait
from omutsulib.native_enums.buffs import NativeBuff
from omutsulib.native_enums.traits import NativeTrait
from omutsulib.services.cas_service import OmutsuCasPart
from omutsulib.utils.singletons import EMPTY_DICT
from omutsulib.wrappers.sim.age import OmutsuAge
# from omutsulib.wrappers.sim.sim import OmutsuSim
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required
from sims.outfits.outfit_enums import OutfitCategory, BodyType
import sims4.log

outfit_categories_excluded_from_diaper = [OutfitCategory.SWIMWEAR,OutfitCategory.BATHING,OutfitCategory.SPECIAL]

force_diaper_pants_buffs = {}
force_diaper_accessory_buffs = {IwnBedwettingBuff.MANDATORY_PADDING}
remove_diaper_buffs = {NativeBuff.POOLS_HYGIENE, NativeBuff.SIMIS_SWIMMING, NativeBuff.SIM_IS_IN_BATH}

_male_bottom = frozenset(DiaperCC.get_filtered_cas_ids(body_type=DiaperBodyType.BOTTOM, height=DiaperHeight.WALL, frame=DiaperFrame.MASCULINE))

_male_accessory = frozenset(DiaperCC.get_filtered_cas_ids(body_type=DiaperBodyType.ACCESSORY, height=DiaperHeight.WALL, frame=DiaperFrame.MASCULINE))

_female_bottom = frozenset(DiaperCC.get_filtered_cas_ids(body_type=DiaperBodyType.BOTTOM, height=DiaperHeight.WALL, frame=DiaperFrame.FEMININE))

_female_accessory = frozenset(DiaperCC.get_filtered_cas_ids(body_type=DiaperBodyType.ACCESSORY, height=DiaperHeight.WALL, frame=DiaperFrame.FEMININE))

logger = sims4.log.Logger('IWNBedwettingMain')


class _OmutsuSimDiaperMixin(_SuperOmutsuSim):

    @sim_info_required(default=False)
    def is_wearing_diaper(self):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        omutsu_sim = OmutsuSim(self)
        current_outfit = omutsu_sim.get_current_outfit()
        if current_outfit is not None and current_outfit[0] == OutfitCategory.BATHING:
            return False

        if omutsu_sim.has_buff(IwnBedwettingBuff.MANDATORY_PADDING):
            return True

        for buff in remove_diaper_buffs:
            if omutsu_sim.has_buff(buff):
                return False

        wetness = omutsu_sim.get_statistic_value(IwnBedwettingStatistic.DIAPER_WETNESS) or 0
        messiness = omutsu_sim.get_statistic_value(IwnBedwettingStatistic.DIAPER_WETNESS) or 0

        if wetness > 0 or messiness > 0:
            return True

        if omutsu_sim.has_trait(IwnBedwettingTrait.SLEEPS_IN_DIAPERS) and (omutsu_sim.has_buff(NativeBuff.MOOD_HIDDEN_ASLEEP) or omutsu_sim.has_buff(NativeBuff.SIM_IS_SLEEPING) or omutsu_sim.has_buff(NativeBuff.SIM_IS_SLEEPING_HIDDEN)):
            return True

        if omutsu_sim.always_wears_diapers():
            return True
        if omutsu_sim.wearing_diaper_item():
            return True

        return False

    @sim_info_required(default=False)
    def always_wears_diapers(self):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        omutsu_sim = OmutsuSim(self)
        if omutsu_sim.has_trait(IwnBedwettingTrait.NEVER_POTTY_TRAINED, IwnBedwettingTrait.DIAPERED_247, IwnBedwettingTrait.DIAPERED_247_MEDICAL, IwnBedwettingTrait.DIAPER_PUNISHED):
            return True
        return False

    @sim_info_required(default=False)
    def wearing_diaper_item(self):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        omutsu_sim = OmutsuSim(self)
        return omutsu_sim.has_trait(IwnBedwettingTrait.WEARING_DIAPER_ITEM)

    @sim_info_required()
    def remove_diaper(self, force_remove=False, outfit_category_and_index=None, update_client=True):
        # if not _ember_detected:
        #     return
        try:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            omutsu_sim = OmutsuSim(self)
            for buff in remove_diaper_buffs:
                if omutsu_sim.has_buff(buff):
                    force_remove = True
            if not force_remove:
                if omutsu_sim.is_wearing_diaper():
                    return
                # if always_wears_diapers(owner_id):
                #     return
                # for buff in force_diaper_pants_buffs:
                #     if has_buff(owner_id, buff):
                #         return
                # for buff in force_diaper_accessory_buffs:
                #     if has_buff(owner_id, buff):
                #         return
            if not omutsu_sim.is_human():
                return
            logger.info("remove_diaper: {}", omutsu_sim)
            if outfit_category_and_index is None:
                outfit_category_and_index = omutsu_sim.get_current_outfit()
            if outfit_category_and_index is not None:
                if not force_remove:
                    if outfit_category_and_index[0] in outfit_categories_excluded_from_diaper:
                        return
                # logger.info('current_outfit: {}'.format(current_outfit))
                outfit_parts = omutsu_sim.get_outfit_parts(outfit_category_and_index)
                if outfit_parts is not None:
                    need_update = False

                    if BodyType.LOWER_BODY in outfit_parts.keys():
                        part_ids_to_remove = set()
                        for outfit_part in outfit_parts[BodyType.LOWER_BODY]:
                            if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                                need_update = True
                                part_ids_to_remove.add(outfit_part.cas_part)
                                logger.info("remove_diaper on LOWER_BODY: {}", omutsu_sim)
                        outfit_parts[BodyType.LOWER_BODY] = tuple(x for x in outfit_parts[BodyType.LOWER_BODY] if x.cas_part not in part_ids_to_remove)
                        if len(outfit_parts[BodyType.LOWER_BODY]) == 0:
                            from omutsulib.utils.nude_body_parts import get_sim_default_nude_cas_part_id
                            outfit_parts[BodyType.LOWER_BODY] = (OmutsuCasPart(get_sim_default_nude_cas_part_id(omutsu_sim,BodyType.LOWER_BODY)),)
                    if BodyType.INDEX_FINGER_LEFT in outfit_parts.keys():
                        part_ids_to_remove = set()
                        for outfit_part in outfit_parts[BodyType.INDEX_FINGER_LEFT]:
                            if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                                need_update = True
                                part_ids_to_remove.add(outfit_part.cas_part)
                                logger.info("remove_diaper on INDEX_FINGER_LEFT: {}", omutsu_sim)
                        outfit_parts[BodyType.INDEX_FINGER_LEFT] = tuple(x for x in outfit_parts[BodyType.INDEX_FINGER_LEFT] if x.cas_part not in part_ids_to_remove)
                    # if iwnbedwetting.main._admin_flag and omutsu_sim.is_child() and BodyType.INDEX_FINGER_LEFT in outfit_parts.keys():
                    #     part_ids_to_remove = set()
                    #     for outfit_part in outfit_parts[BodyType.INDEX_FINGER_LEFT]:
                    #         if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                    #             need_update = True
                    #             part_ids_to_remove.add(outfit_part.cas_part)
                    #             logger.info("remove_diaper on INDEX_FINGER_LEFT: {}", omutsu_sim)
                    #     outfit_parts[BodyType.INDEX_FINGER_LEFT] = tuple(x for x in outfit_parts[BodyType.INDEX_FINGER_LEFT] if x.cas_part not in part_ids_to_remove)
                    if need_update:
                        omutsu_sim.set_outfit_parts(outfit_category_and_index, outfit_parts, update_client)
        except Exception as e:
            logger.error("remove_diaper failed to run.")
            logger.error(traceback.format_exc())

    @sim_info_required(default=False)
    def have_pants_changed(self, current_outfit, previous_outfit):
        if current_outfit is not None and previous_outfit is not None:
            if previous_outfit[0] == current_outfit[0] and previous_outfit[1] == current_outfit[1]:
                return False
            from omutsulib.wrappers.sim.sim import OmutsuSim
            omutsu_sim = OmutsuSim(self)
            current_parts = omutsu_sim.get_outfit_parts(current_outfit)
            previous_parts = omutsu_sim.get_outfit_parts(previous_outfit)

            logger.info("previous outfit {}", previous_outfit)

            logger.info("current outfit: {}", current_outfit)

            logger.info("previous parts {}", previous_parts)

            logger.info("current parts: {}", current_parts)

            if current_parts is not None and previous_parts is not None:
                if BodyType.LOWER_BODY in current_parts.keys():
                    if BodyType.LOWER_BODY not in previous_parts.keys():
                        return True
                    if current_parts[BodyType.LOWER_BODY] != previous_parts[BodyType.LOWER_BODY]:
                        logger.info("LOWER_BODY CAS part changed")
                        logger.info("Previous part {}", previous_parts[BodyType.LOWER_BODY])
                        logger.info("Current part {}", current_parts[BodyType.LOWER_BODY])
                        return True
                    else:
                        logger.info("LOWER_BODY CAS part not changed")
                        return False
                elif BodyType.FULL_BODY in current_parts.keys():
                    if BodyType.FULL_BODY not in previous_parts.keys():
                        return True
                    if current_parts[BodyType.FULL_BODY] != previous_parts[BodyType.FULL_BODY]:
                        logger.info("FULL_BODY CAS part changed")
                        logger.info("Previous part {}", previous_parts[BodyType.FULL_BODY])
                        logger.info("Current part {}", current_parts[BodyType.FULL_BODY])
                        return True
                else:
                    if BodyType.LOWER_BODY in previous_parts.keys():
                        return True
                    if BodyType.FULL_BODY in previous_parts.keys():
                        return True
        return False

    @sim_info_required(default=EMPTY_DICT)
    def get_diaper_parts(self, outfit_category_and_index, include_bottom:bool=True, include_accessory:bool=True):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        omutsu_sim = OmutsuSim(self)
        outfit_parts = omutsu_sim.get_outfit_parts(outfit_category_and_index)
        diaper_parts = {}
        if outfit_parts is not None:
            if include_bottom:
                if BodyType.LOWER_BODY in outfit_parts.keys():
                    for outfit_part in outfit_parts[BodyType.LOWER_BODY]:
                        if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                            diaper_parts[BodyType.LOWER_BODY] = outfit_part
                            break
            if include_accessory:
                if BodyType.INDEX_FINGER_LEFT in outfit_parts.keys():
                    for outfit_part in outfit_parts[BodyType.INDEX_FINGER_LEFT]:
                        if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                            diaper_parts[BodyType.INDEX_FINGER_LEFT] = outfit_part
                            break
        return diaper_parts

    @sim_info_required(default=False)
    def is_diaper_removed(self, current_outfit, previous_outfit):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        omutsu_sim = OmutsuSim(self)
        return omutsu_sim.is_diaper_accessory_removed(current_outfit, previous_outfit) or omutsu_sim.is_diaper_bottom_removed(current_outfit, previous_outfit)

    @sim_info_required(default=False)
    def is_diaper_accessory_removed(self, current_outfit, previous_outfit):
        if current_outfit is not None and previous_outfit is not None:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            omutsu_sim = OmutsuSim(self)
            # if previous_outfit[0] == current_outfit[0] and previous_outfit[1] == current_outfit[1]:
            #     return False
            current_parts = omutsu_sim.get_outfit_parts(current_outfit)
            previous_parts = omutsu_sim.get_outfit_parts(previous_outfit)

            logger.info("previous outfit {}", previous_outfit)

            logger.info("current outfit: {}", current_outfit)

            logger.info("previous parts {}", previous_parts)

            logger.info("current parts: {}", current_parts)

            had_diaper = False

            if current_parts is not None and previous_parts is not None:
                if BodyType.INDEX_FINGER_LEFT in previous_parts.keys():
                    for outfit_part in previous_parts[BodyType.INDEX_FINGER_LEFT]:
                        if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                            had_diaper = True
                            break
                    if had_diaper:
                        if BodyType.INDEX_FINGER_LEFT not in current_parts.keys():
                            return True
                        for outfit_part in current_parts[BodyType.INDEX_FINGER_LEFT]:
                            if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                                return False
                        return True
                # if iwnbedwetting.main._admin_flag and omutsu_sim.is_child() and BodyType.INDEX_FINGER_LEFT in previous_parts.keys():
                #     for outfit_part in previous_parts[BodyType.INDEX_FINGER_LEFT]:
                #         if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                #             had_diaper = True
                #             break
                #     if had_diaper:
                #         if BodyType.INDEX_FINGER_LEFT not in current_parts.keys():
                #             return True
                #         for outfit_part in current_parts[BodyType.INDEX_FINGER_LEFT]:
                #             if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                #                 return False
                #         return True

        return False

    @sim_info_required(default=False)
    def is_diaper_bottom_removed(self, current_outfit, previous_outfit):
        if current_outfit is not None and previous_outfit is not None:
            # if previous_outfit[0] == current_outfit[0] and previous_outfit[1] == current_outfit[1]:
            #     return False
            from omutsulib.wrappers.sim.sim import OmutsuSim
            omutsu_sim = OmutsuSim(self)
            current_parts = omutsu_sim.get_outfit_parts(current_outfit)
            previous_parts = omutsu_sim.get_outfit_parts(previous_outfit)

            logger.info("previous outfit {}", previous_outfit)

            logger.info("current outfit: {}", current_outfit)

            logger.info("previous parts {}", previous_parts)

            logger.info("current parts: {}", current_parts)

            had_diaper = False

            if current_parts is not None and previous_parts is not None:
                if BodyType.LOWER_BODY in previous_parts.keys():
                    for outfit_part in previous_parts[BodyType.LOWER_BODY]:
                        if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                            had_diaper = True
                            break
                    if had_diaper:
                        if BodyType.LOWER_BODY not in current_parts.keys():
                            return True
                        for outfit_part in current_parts[BodyType.LOWER_BODY]:
                            if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                                return False
                        return True
        return False

    @sim_info_required(default=EMPTY_DICT)
    def get_modified_diaper_outfit_parts(self, outfit_category_and_index, wetness_level, mess_level):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        omutsu_sim = OmutsuSim(self)
        outfit_parts = omutsu_sim.get_outfit_parts(outfit_category_and_index)

        if outfit_parts is None:
            return EMPTY_DICT

        needs_outfit_change = False

        for body_type, outfit_part_tuple in outfit_parts.items():
            # if isinstance(outfit_part, tuple):
            #     outfit_part = outfit_part[0]
            for outfit_part in outfit_part_tuple:
                if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                    base_config = DiaperLoadCASConfig.get_diaper_config(outfit_part.cas_part)

                    if base_config is not None:
                        if body_type != base_config.body_type:
                            continue
                        logger.info('supported diaper {} found in slot {}', outfit_part, base_config.body_type)
                        if wetness_level < 1 and mess_level < 1:
                            logger.info('clean diaper detected')
                            if outfit_part.cas_part != base_config.default_cas_part:
                                outfit_part.cas_part = base_config.default_cas_part
                                needs_outfit_change = True
                                logger.info('changing to clean diaper part {}', base_config.default_cas_part)
                            else:
                                logger.info("Already wearing part")
                        elif mess_level < 1:
                            logger.info('wet diaper detected')
                            filtered_parts = [x for x in base_config.diaper_load_config if x.mess_level < 1 and x.wetness_level <= wetness_level]

                            logger.info('possible parts {}', filtered_parts)

                            if len(filtered_parts) > 0:
                                new_part = filtered_parts[0]
                                for part in filtered_parts:
                                    if new_part.wetness_level < part.wetness_level <= wetness_level:
                                        new_part = part
                                if new_part is not None:
                                    if outfit_part.cas_part != new_part.cas_part:
                                        logger.info('changing to wet diaper part {}', new_part.cas_part)
                                        outfit_part.cas_part = new_part.cas_part
                                        needs_outfit_change = True
                                    else:
                                        logger.info("Already wearing part")
                            else:
                                logger.info("no valid part found")
                        elif wetness_level < 1:
                            logger.info('messy diaper detected')
                            filtered_parts = [x for x in base_config.diaper_load_config if x.wetness_level < 1 and x.mess_level <= mess_level]

                            logger.info('possible parts {}', filtered_parts)

                            if len(filtered_parts) > 0:
                                new_part = filtered_parts[0]
                                for part in filtered_parts:
                                    if new_part.mess_level < part.mess_level <= mess_level:
                                        new_part = part
                                if new_part is not None:
                                    if outfit_part.cas_part != new_part.cas_part:
                                        logger.info('changing to messy diaper part {}', new_part.cas_part)
                                        outfit_part.cas_part = new_part.cas_part
                                        needs_outfit_change = True
                                    else:
                                        logger.info("Already wearing part")
                            else:
                                logger.info("no valid part found")
                        else:
                            best_wet_level = max(x.wetness_level for x in base_config.diaper_load_config if
                                                 x.wetness_level <= wetness_level and x.mess_level <= mess_level)
                            best_mess_level = max(x.mess_level for x in base_config.diaper_load_config if
                                                  x.wetness_level == best_wet_level and x.mess_level <= mess_level)
                            filtered_parts = [x.cas_part for x in base_config.diaper_load_config if
                                              x.mess_level == best_mess_level and x.wetness_level == best_wet_level]
                            if len(filtered_parts) > 0:
                                new_part = filtered_parts[0]
                                if new_part is not None:
                                    if outfit_part.cas_part != new_part:
                                        logger.info('changing to wet & messy diaper part {}', new_part)
                                        outfit_part.cas_part = new_part
                                        needs_outfit_change = True
                                    else:
                                        logger.info("Already wearing part")

        if needs_outfit_change:
            return outfit_parts
        return None

    @sim_info_required()
    def apply_outfit_parts_for_diaper_load(self, outfit_category_and_index=None, update_client=True):
        try:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            omutsu_sim = OmutsuSim(self)
            logger.info("apply_outfit_parts_for_diaper_load: {}", self)
            wetness_level = omutsu_sim.get_statistic_value(IwnBedwettingStatistic.DIAPER_WETNESS) or 0
            mess_level = omutsu_sim.get_statistic_value(IwnBedwettingStatistic.DIAPER_MESSINESS) or 0
            logger.info("diaper wetness: {}", wetness_level)
            logger.info("diaper messiness: {}", mess_level)

            if outfit_category_and_index is None:
                outfit_category_and_index = omutsu_sim.get_current_outfit()

            # original_parts = omutsu_sim.get_outfit_parts(outfit_category_and_index)

            # logger.info("original_parts {}", original_parts)

            modified_parts = omutsu_sim.get_modified_diaper_outfit_parts(outfit_category_and_index, wetness_level, mess_level)

            if modified_parts is not None:
                omutsu_sim.set_outfit_parts(outfit_category_and_index, modified_parts, update_client)
        except Exception as e:
            logger.error("apply_outfit_parts_for_diaper_load encountered an error.")
            logger.error(traceback.format_exc())

    @sim_info_required()
    def put_on_random_diaper_bottom(self, object_instance_id=None, remove_full_body: bool = False, remove_tights: bool = False, remove_top: bool = False, outfit_category_and_index=None, update_client=True):
        if not iwnbedwetting.main._ember_detected:
            return
        try:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            omutsu_sim = OmutsuSim(self)
            if not omutsu_sim.is_human():
                return
            logger.info("iwn.put_on_random_diaper_bottom: {}", omutsu_sim)
            if outfit_category_and_index is None:
                outfit_category_and_index = omutsu_sim.get_current_outfit()
            if outfit_category_and_index is not None:
                if outfit_category_and_index[0] in outfit_categories_excluded_from_diaper:
                    return
                # logger.info('current_outfit: {}'.format(current_outfit))
                outfit_parts = omutsu_sim.get_outfit_parts(outfit_category_and_index)
                if outfit_parts is not None:

                    if remove_full_body:
                        outfit_parts.pop(BodyType.FULL_BODY, None)

                    if remove_tights:
                        outfit_parts.pop(BodyType.TIGHTS, None)

                    if remove_top:
                        outfit_parts.pop(BodyType.UPPER_BODY, None)

                    if BodyType.FULL_BODY in outfit_parts.keys():
                        omutsu_sim.put_on_random_diaper_accessory()
                        return

                    if BodyType.LOWER_BODY in outfit_parts.keys():
                        for outfit_part in outfit_parts[BodyType.LOWER_BODY]:
                            if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                                return
                    else:
                        outfit_parts[BodyType.LOWER_BODY] = (OmutsuCasPart(0),)

                    diaper_part_id = None

                    default_diaper_type = omutsu_sim.get_statistic_value(IwnBedwettingStatistic.DEFAULT_DIAPER_TYPE)

                    if default_diaper_type is not None:
                        default_diaper_type = int(default_diaper_type)
                        default_cas_ids = DiaperCC.get_filtered_cas_ids(height=DiaperHeight.WALL, body_type=DiaperBodyType.BOTTOM, frame=omutsu_sim.get_diaper_frame_for_sim(), diaper_type=default_diaper_type)
                        if len(default_cas_ids) > 0:
                            logger.info("Looking up diaper part by default diaper type")
                            diaper_part_id = random.choice(
                                DiaperLoadCASConfig.get_default_diaper_parts_ids_for_body_type(BodyType.LOWER_BODY,
                                                                                               default_cas_ids))
                    if diaper_part_id is None:
                        if omutsu_sim.is_teen_or_older():
                            if omutsu_sim.has_trait(NativeTrait.GENDER_OPTIONS_FRAME_MASCULINE):
                                diaper_part_id = random.choice(
                                    DiaperLoadCASConfig.get_default_diaper_parts_ids_for_body_type(BodyType.LOWER_BODY,
                                                                                                   _male_bottom))
                            elif omutsu_sim.has_trait(NativeTrait.GENDER_OPTIONS_FRAME_FEMININE):
                                diaper_part_id = random.choice(
                                    DiaperLoadCASConfig.get_default_diaper_parts_ids_for_body_type(BodyType.LOWER_BODY,
                                                                                                   _female_bottom))
                        elif iwnbedwetting.main._admin_flag and omutsu_sim.is_child():
                            diaper_part_id = 17916267921504688060
                    if diaper_part_id is not None:
                        outfit_parts[BodyType.LOWER_BODY] = (OmutsuCasPart((diaper_part_id)),)
                        outfit_parts.pop(BodyType.INDEX_FINGER_LEFT, None)
                        omutsu_sim.set_outfit_parts(outfit_category_and_index, outfit_parts, update_client)
        except Exception as e:
            logger.error("put_on_random_diaper_bottom failed to run.")
            logger.error(traceback.format_exc())

    @sim_info_required()
    def update_default_diaper(self, force_change: bool = False):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        omutsu_sim = OmutsuSim(self)
        if not omutsu_sim.has_trait(IwnBedwettingTrait.NO_VISIBLE_DIAPERS):
            omutsu_sim.put_on_random_diaper_accessory(force_change=True)

    @sim_info_required()
    def put_on_random_diaper_accessory(self, object_instance_id=None, outfit_category_and_index=None, update_client=True, force_change=False):
        if not iwnbedwetting.main._ember_detected:
            return
        try:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            omutsu_sim = OmutsuSim(self)
            # logger.info(str(owner_id))
            if not omutsu_sim.is_human():
                return
            logger.info("iwn.put_on_random_diaper_accessory: {}", omutsu_sim)

            object_definition_id = None

            if object_instance_id is not None:
                object_instance_id = int(object_instance_id)
                object_instance = services.object_manager().get(object_instance_id) or services.inventory_manager().get(object_instance_id)
                if object_instance is not None:
                    object_definition_id = object_instance.definition.id
                    logger.info("Object definition found")

            if outfit_category_and_index is None:
                outfit_category_and_index = omutsu_sim.get_current_outfit()
            if outfit_category_and_index is not None:
                if outfit_category_and_index[0] in outfit_categories_excluded_from_diaper:
                    return
                outfit_parts = omutsu_sim.get_outfit_parts(outfit_category_and_index)
                if outfit_parts is not None:
                    if BodyType.LOWER_BODY in outfit_parts.keys():
                        for outfit_part in outfit_parts[BodyType.LOWER_BODY]:
                            if not force_change and object_definition_id is None and DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                                return

                    if BodyType.INDEX_FINGER_LEFT in outfit_parts.keys():
                        for outfit_part in outfit_parts[BodyType.INDEX_FINGER_LEFT]:
                            if not force_change and object_definition_id is None and DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                                if object_definition_id is None:
                                    return
                    else:
                        outfit_parts[BodyType.INDEX_FINGER_LEFT] = (OmutsuCasPart(0),)

                    diaper_part_id = None

                    body_type = BodyType.INDEX_FINGER_LEFT

                    default_diaper_type = omutsu_sim.get_statistic_value(IwnBedwettingStatistic.DEFAULT_DIAPER_TYPE)
                    logger.info("Default diaper type: {}".format(default_diaper_type))

                    default_cas_ids = []

                    if default_diaper_type is not None:
                        default_diaper_type = int(default_diaper_type)
                        default_cas_ids = DiaperCC.get_filtered_cas_ids(height=DiaperHeight.WALL, body_type=DiaperBodyType.ACCESSORY, frame=omutsu_sim.get_diaper_frame_for_sim(), diaper_type=default_diaper_type)

                    if omutsu_sim.is_teen_or_older():
                        if omutsu_sim.has_trait(NativeTrait.GENDER_OPTIONS_FRAME_MASCULINE):
                            if object_definition_id is not None:
                                rec_part_ids = DiaperCC.get_by_object_definition(object_definition_id, frame=DiaperFrame.MASCULINE, body_type=DiaperBodyType.ACCESSORY)
                                if len(rec_part_ids) > 0:
                                        logger.info("Looking up diaper part by object definition")
                                        diaper_part_id = random.choice(
                                            DiaperLoadCASConfig.get_default_diaper_parts_ids_for_body_type(BodyType.INDEX_FINGER_LEFT,
                                                                                                           rec_part_ids))
                                elif len(default_cas_ids) > 0:
                                    logger.info("Looking up diaper part by default diaper type")
                                    diaper_part_id = random.choice(
                                        DiaperLoadCASConfig.get_default_diaper_parts_ids_for_body_type(BodyType.INDEX_FINGER_LEFT,
                                                                                                       default_cas_ids))
                                if diaper_part_id is None:
                                    diaper_part_id = random.choice(
                                        DiaperLoadCASConfig.get_default_diaper_parts_ids_for_body_type(BodyType.INDEX_FINGER_LEFT,
                                                                                                       _male_accessory))
                        elif omutsu_sim.has_trait(NativeTrait.GENDER_OPTIONS_FRAME_FEMININE):
                            if object_definition_id is not None:
                                rec_part_ids = DiaperCC.get_by_object_definition(object_definition_id, frame=DiaperFrame.FEMININE, body_type=DiaperBodyType.ACCESSORY)
                                if len(rec_part_ids) > 0:
                                    logger.info("Looking up diaper part by object definition")
                                    diaper_part_id = random.choice(
                                        DiaperLoadCASConfig.get_default_diaper_parts_ids_for_body_type(BodyType.INDEX_FINGER_LEFT,
                                                                                                       rec_part_ids))
                            elif len(default_cas_ids) > 0:
                                logger.info("Looking up diaper part by default diaper type")
                                diaper_part_id = random.choice(
                                    DiaperLoadCASConfig.get_default_diaper_parts_ids_for_body_type(BodyType.INDEX_FINGER_LEFT,
                                                                                                   default_cas_ids))
                            if diaper_part_id is None:
                                diaper_part_id = random.choice(
                                    DiaperLoadCASConfig.get_default_diaper_parts_ids_for_body_type(BodyType.INDEX_FINGER_LEFT,
                                                                                                   _female_accessory))
                    elif iwnbedwetting.main._admin_flag and omutsu_sim.is_child():
                        diaper_part_id = 16089036029714611952
                        body_type = BodyType.INDEX_FINGER_LEFT
                    if diaper_part_id is not None:
                        outfit_parts[body_type] = (OmutsuCasPart(diaper_part_id),)
                        omutsu_sim.set_outfit_parts(outfit_category_and_index, outfit_parts, update_client)
        except Exception as e:
            logger.error("put_on_random_diaper_accessory failed to run.")
            logger.error(traceback.format_exc())

    @sim_info_required(default=DiaperFrame.INVALID)
    def get_diaper_frame_for_sim(self):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        omutsu_sim = OmutsuSim(self)
        if omutsu_sim.get_age() == OmutsuAge.CHILD:
            return DiaperFrame.CHILD
        if omutsu_sim.has_trait(NativeTrait.GENDER_OPTIONS_FRAME_MASCULINE):
            return DiaperFrame.MASCULINE
        if omutsu_sim.has_trait(NativeTrait.GENDER_OPTIONS_FRAME_FEMININE):
            return DiaperFrame.FEMININE
        return DiaperFrame.INVALID
