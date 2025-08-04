import os
import random
import traceback
import urllib
import urllib.error
import urllib.request
import urllib.response
import webbrowser

import objects
import objects.components.types
import services
import sims4.callback_utils
import sims4.commands
import sims4.log
import sims4.reload
from autonomy.autonomy_modifier import AutonomyModifier
from clock import ClockSpeedMode
from clubs.club_tuning import ClubRuleCriteriaTrait, ClubTunables
from distributor.shared_messages import IconInfoData
from event_testing.tests import CompoundTestList, TestList
from interactions import ParticipantType
from interactions.base.basic import FlexibleLengthContent
from interactions.utils.loot_element import LootElement
from interactions.utils.statistic_element import ExitCondition
from omutsulib.enums.buffs import IwnBedwettingBuff
from omutsulib.enums.interactions import InteractionSets, DiaperInteraction, BedwettingInteraction, DiaperChangeInteraction
from omutsulib.enums.pacifiers import AdultPacifiers, ChildPacifiers
from omutsulib.enums.rewards import IwnBedwettingReward
from omutsulib.enums.snippets import IwnBedwettingTestSet
from omutsulib.enums.statistics import IwnBedwettingStatistic, DiaperStateStatistics
from omutsulib.enums.traits import IwnBedwettingTrait
from omutsulib.enums.wickedwhims import WW_SimStatistic, WW_SexNakedType, WW_SexUndressingTypeSetting
from omutsulib.native_enums.buffs import NativeBuff
from omutsulib.native_enums.interactions import NativeInteraction
from omutsulib.native_enums.motives import NativeMotive
from omutsulib.services.cas_service import OmutsuCasPart
from omutsulib.services.satisfaction_service import get_satisfaction_service
from omutsulib.services.statistics_service import get_statistics_service
from omutsulib.utils.injector import inject
from omutsulib.utils.paths import get_sims_mods_directory
from omutsulib.wrappers.sim.diaper import remove_diaper_buffs, force_diaper_pants_buffs, force_diaper_accessory_buffs
from omutsulib.wrappers.sim.sim import OmutsuSim
from satisfaction.satisfaction_tracker import SatisfactionTracker
from sims.outfits.outfit_enums import BodyType, OutfitCategory
from sims.sim_info import SimInfo
from sims.sim_info_tests import BuffTest
from sims.sim_info_types import Age, Species
from sims4 import resources, collections
from sims4.collections import make_immutable_slots_class
from sims4.localization import LocalizationHelperTuning
from sims4.resources import Types
from sims4.tuning.instance_manager import InstanceManager
from sims4.tuning.tunable import TunableFactory
from statistics.statistic_ops import StatisticChangeOp
from tag import Tag
from ui.ui_dialog import UiDialogOk, UiDialogResponse, ButtonType
from ui.ui_dialog_notification import UiDialogNotification
from zone import Zone

IWN_BED_WETTING_VERSION = "2.3.0"
PACKAGE_VERSION = 3
ModHasRun = False
devMode = False
logger = sims4.log.Logger('IWNBedwettingMain')

old_mod_packages = ('LilNinthel_ABDL_Diaper_Change.package','LilNinthel_ABDL_Uppies.package','LilNinthel_Adult_Diaper_Object.package','LilNinthel_Toddler_Social_Animations.package','LilNinthel_UseDiaper_Animations.package')

old_addons = ('Extended BabyLola Happily Diapered','Extended HappilyMessy_DiaperDump','Extended Lil Luna Unhappily Diapered','Extended mackico ABDL')

_old_mods_detected = False
_old_addons_detected = False
_ember_detected = False
_duplicate_mods = False
_admin_flag = False

# xml_injector_spec = importlib.util.find_spec("xml_injector")
# _xml_injector_found = xml_injector_spec is not None

try:
    import wickedwhims.nudity.outfit_nudity_reason
    _wicked_whims_installed = True
    from wickedwhims.sex.generic.utils.state import is_sim_in_sex_interaction, is_sim_going_to_sex_interaction
    from turbolib2.wrappers.sim.sim import TurboSim
    # import wickedwhims.nudity.body.sim_outfit_utils as ww_outfit_utils
    from wickedwhims.nudity.body.sim_outfit_utils import strip_outfit, _wickedwhims_register_nudity_outfit_change_callback, _wickedwhims_register_nudity_outfit_change_callback_on_new_sim
    import wickedwhims.sex.integral.sex_handlers.active_sex.utils.outfit as ww_sex_outfit
    from wickedwhims.sex.integral.sex_handlers.active_sex.utils.outfit import update_sim_sex_outfit
    from wickedwhims.sex.integral.sex_handlers.active_sex.active_sex_handlers import get_active_sex_instance
    from wickedwhims.sex.sex_settings import get_sex_setting, SexSetting
    # from wickedwhims.sex.generic.interactions.instant_undressing import _UndressActorBodyTypesInteraction

    # logger.info(str(inspect.signature(strip_outfit)))

except Exception:
    logger.error("Error importing WickedWhims modules")
    logger.error(traceback.format_exc())
    _wicked_whims_installed = False

_admin_package = 'LilNinthel_AdminOverrides.package'


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

mod_files_names = set()
duplicated_mod_files_names = set()
mods_dict = dict()
old_files = set()
old_addon_files = set()


def detect_mods():
    global _old_mods_detected
    global _old_addons_detected
    global _admin_flag
    global _ember_detected
    global _duplicate_mods

    for dirpath, __, files in os.walk(get_sims_mods_directory()):
        for file_name in files:
            if file_name.lower().endswith('.package'):
                if file_name.lower().startswith('LilNinthel_'.lower()) and file_name.lower() != 'LilNinthel_IWNBedwetting_Extended_Plus.package'.lower():
                    if not _admin_flag:
                        _old_mods_detected = True
                        old_files.add(file_name)
                if file_name.startswith('[Ember]') and file_name.endswith('accessory.package'):
                    _ember_detected = True
                if not file_name.lower() in mods_dict.keys():
                    mods_dict[file_name.lower()] = []
                # mod_dict[file_name.lower()].append(os.path.join(remove_prefix(dirpath,get_sims_mods_directory()),file_name))
                mods_dict[file_name.lower()].append(remove_prefix(dirpath, get_sims_mods_directory()))
                for prefix in old_addons:
                    if file_name.lower().startswith(prefix.lower()):
                        _old_addons_detected = True
                        old_addon_files.add(file_name)
                if file_name == _admin_package:
                    _admin_flag = True
                    _old_mods_detected = False
                    _old_files = set()
                    logger.info('Admin mode activated')
                if file_name.lower() in mod_files_names:
                    duplicated_mod_files_names.add(file_name)
                    _duplicate_mods = True
                else:
                    mod_files_names.add(file_name.lower())


# def get_mods_files_info():
#     return (
#      sorted(mod_files_names), sorted(duplicated_mod_files_names), sorted(old_files), mod_dict, old_addon_files)

@inject(InstanceManager, 'load_data_into_class_instances')
def _load_satisfaction_store_rewards(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        if self.TYPE == Types.REWARD:
            logger.info('Registering reward store items')

            get_satisfaction_service().register_store_reward(IwnBedwettingReward.BEDWETTER, 100, SatisfactionTracker.SatisfactionAwardTypes.TRAIT)
            get_satisfaction_service().register_store_reward(IwnBedwettingReward.INCONTINENCE, 100, SatisfactionTracker.SatisfactionAwardTypes.TRAIT)
            get_satisfaction_service().register_store_reward(IwnBedwettingReward.DIAPER_CURIOUS, 100, SatisfactionTracker.SatisfactionAwardTypes.TRAIT)
            get_satisfaction_service().register_store_reward(IwnBedwettingReward.PANTS_WETTER, 100, SatisfactionTracker.SatisfactionAwardTypes.TRAIT)
            get_satisfaction_service().register_store_reward(IwnBedwettingReward.PANTS_POOPER, 100, SatisfactionTracker.SatisfactionAwardTypes.TRAIT)
            get_satisfaction_service().register_store_reward(IwnBedwettingReward.DESPERATION_ENTHUSIAST, 100, SatisfactionTracker.SatisfactionAwardTypes.TRAIT)
            get_satisfaction_service().register_store_reward(IwnBedwettingReward.LITTLE, 100, SatisfactionTracker.SatisfactionAwardTypes.TRAIT)
            get_satisfaction_service().register_store_reward(IwnBedwettingReward.TOILET_BAN, 100, SatisfactionTracker.SatisfactionAwardTypes.TRAIT)
            get_satisfaction_service().register_store_reward(IwnBedwettingReward.DIAPER_DEPENDENT, 100, SatisfactionTracker.SatisfactionAwardTypes.TRAIT)
            get_satisfaction_service().register_store_reward(IwnBedwettingReward.DIAPERED_247, 100, SatisfactionTracker.SatisfactionAwardTypes.TRAIT)
            get_satisfaction_service().register_store_reward(IwnBedwettingReward.UNIVERSAL_CAREGIVER, 100, SatisfactionTracker.SatisfactionAwardTypes.TRAIT)

    except Exception as e:
        logger.error("InstanceManager.load_data_into_class_instances injection failed to run.")
        logger.error(traceback.format_exc())

    return result


def add_diaper_load_tracking(sim_info):
    trackers = []
    wrapper = DiaperWatcherWrapper(sim_info)
    trackers.append(get_statistic_tracker(sim_info, IwnBedwettingStatistic.DIAPER_WETNESS))
    trackers.append(get_statistic_tracker(sim_info, IwnBedwettingStatistic.DIAPER_MESSINESS))
    trackers.append(get_statistic_tracker(sim_info, IwnBedwettingStatistic.DIAPER_DEPENDENCE))
    sex_tracker = get_statistic_tracker(sim_info, WW_SimStatistic.WW_SEX_ACTIVE_INSTANCE_IDENTIFIER)
    if sex_tracker is not None:
        sex_tracker.add_watcher(wrapper.wicked_whims_stat_watcher)
        sex_tracker.add_on_remove_callback(wrapper.wicked_whims_stat_removed)
    sex_animation_tracker = get_statistic_tracker(sim_info, WW_SimStatistic.WW_SEX_ACTIVE_INSTANCE_ANIMATION_INDEX)
    if sex_animation_tracker is not None:
        sex_animation_tracker.add_watcher(wrapper.wicked_whims_stat_watcher)
        sex_animation_tracker.add_on_remove_callback(wrapper.wicked_whims_stat_removed)
    for tracker in trackers:
        if tracker is not None:
            logger.info("Adding tracker {} to {}".format(tracker, sim_info))
            tracker.add_watcher(wrapper.diaper_load_stat_watcher)
            tracker.add_on_remove_callback(wrapper.on_diaper_load_stat_removed)


def get_diaper_stats_for_state(wetness, messiness):
    stats = []
    if wetness is None:
        wetness = 0
    if messiness is None:
        messiness = 0
    wetness = int(wetness)
    messiness = int(messiness)
    if wetness == 0:
        stats.append(DiaperStateStatistics.DIAPER_STATE_DRY)
    elif wetness == 1:
        stats.append(DiaperStateStatistics.DIAPER_STATE_WETNESS_1)
    elif wetness == 2:
        stats.append(DiaperStateStatistics.DIAPER_STATE_WETNESS_2)
    elif wetness == 3:
        stats.append(DiaperStateStatistics.DIAPER_STATE_WETNESS_3)
    elif wetness == 4:
        stats.append(DiaperStateStatistics.DIAPER_STATE_WETNESS_4)
        stats.append(DiaperStateStatistics.DIAPER_STATE_WETNESS_EXTRA)
        stats.append(DiaperStateStatistics.DIAPER_STATE_WETNESS_SMELL_LIKE_PEE)
    elif wetness == 5:
        stats.append(DiaperStateStatistics.DIAPER_STATE_WETNESS_5)
        stats.append(DiaperStateStatistics.DIAPER_STATE_WETNESS_EXTRA)
        stats.append(DiaperStateStatistics.DIAPER_STATE_WETNESS_SMELL_LIKE_PEE)
    elif wetness >= 6:
        stats.append(DiaperStateStatistics.DIAPER_STATE_WETNESS_6)
        stats.append(DiaperStateStatistics.DIAPER_STATE_WETNESS_EXTRA)
        stats.append(DiaperStateStatistics.DIAPER_STATE_WETNESS_SMELL_LIKE_PEE)

    if messiness == 1:
        stats.append(DiaperStateStatistics.DIAPER_STATE_MESSINESS_1)
    elif messiness == 2:
        stats.append(DiaperStateStatistics.DIAPER_STATE_MESSINESS_2)
    elif messiness >= 3:
        stats.append(DiaperStateStatistics.DIAPER_STATE_MESSINESS_3)

    return stats


class DiaperWatcherWrapper:
    def __init__(self, sim_info):
        self.omutsu_sim = OmutsuSim(sim_info)
        self.value_dict = dict()

    def diaper_load_stat_watcher(self, stat_type, old_value, new_value):
        if stat_type.guid64 == IwnBedwettingStatistic.DIAPER_WETNESS or stat_type.guid64 == IwnBedwettingStatistic.DIAPER_MESSINESS:
            try:
                logger.info("diaper_load_stat_watcher {}".format(stat_type))
                if stat_type.guid64 in self.value_dict:
                    logger.info("old {} new {}".format(self.value_dict[stat_type.guid64], new_value))
                    if self.value_dict[stat_type.guid64] == new_value:
                        logger.info("No change in value")
                        return
                self.omutsu_sim.apply_outfit_parts_for_diaper_load()
                self.value_dict[stat_type.guid64] = new_value
                # if stat_type is not None:
                #     logger.info("stat_type {}", stat_type)
                #     logger.info("stat_type {}", stat_type.__class__)
                #     logger.info("stat_type {}", dir(stat_type))
                #     if stat_type.tracker is not None:
                #         logger.info("stat_type.tracker {}", stat_type.tracker)
                #         logger.info("stat_type.tracker {}", stat_type.tracker.__class__)
                #         logger.info("stat_type.tracker {}", dir(stat_type.tracker))
                #         stat = stat_type.tracker.get_statistic(stat_type)
                #
                #         if stat is not None and stat.tracker.owner is not None:
                #             apply_outfit_parts_for_diaper_load(stat.tracker.owner)
            except Exception as e:
                logger.error("diaper_load_stat_watcher failed to run.")
                logger.error(traceback.format_exc())
        elif stat_type.guid64 == IwnBedwettingStatistic.DIAPER_DEPENDENCE:
            if new_value is not None:
                self.omutsu_sim.set_statistic_value(IwnBedwettingStatistic.DIAPER_TRAINING_SKILL, 100 + new_value*124.8)

    def wicked_whims_stat_watcher(self, stat_type, old_value, new_value):
        if stat_type.guid64 == WW_SimStatistic.WW_SEX_ACTIVE_INSTANCE_IDENTIFIER or stat_type.guid64 == WW_SimStatistic.WW_SEX_ACTIVE_INSTANCE_ANIMATION_INDEX or stat_type.guid64 == WW_SimStatistic.WW_IS_SIM_IN_SEX:
            try:
                logger.info("wicked_whims_stat_watcher {}".format(stat_type))
                if stat_type.guid64 in self.value_dict:
                    logger.info("old {} new {}".format(self.value_dict[stat_type.guid64], new_value))
                    if self.value_dict[stat_type.guid64] == new_value:
                        logger.info("No change in value")
                        return

                self.value_dict[stat_type.guid64] = new_value

                keep_diaper = self.omutsu_sim.get_statistic_value(IwnBedwettingStatistic.WW_KEEP_DIAPER_ACCESSORY_DURING_SEX) or 0
                if keep_diaper != 0:
                    return

                active_sex_id = self.omutsu_sim.get_statistic_value(WW_SimStatistic.WW_SEX_ACTIVE_INSTANCE_IDENTIFIER) or 0
                if active_sex_id != 0:
                    sex_instance = get_active_sex_instance(active_sex_id)
                    if sex_instance is not None:
                        # logger.info(str(sex_instance))
                        animation_instance = sex_instance.get_animation_instance()
                        # logger.info(str(animation_instance))
                        if animation_instance is not None:
                            actors = animation_instance.get_actors()
                            if len(actors) > 0:
                                for actor in actors:
                                    sim_id = sex_instance.get_sim_id_by_actor_id(actor.get_actor_id())
                                    if sim_id == self.omutsu_sim.get_sim_id():
                                        # logger.info(str(actor))
                                        # if not has_trait(self.get_sim_id(), visible_diapers_opt_out_trait):
                                        undress_setting = get_sex_setting(SexSetting.SEX_UNDRESSING_TYPE)
                                        npc_undress_setting = get_sex_setting(SexSetting.NPC_SEX_UNDRESSING_TYPE)
                                        # is_npc_only = kwargs.get("is_npc_only", False)
                                        if self.omutsu_sim.is_npc():
                                            undress_setting = npc_undress_setting
                                        if undress_setting != WW_SexUndressingTypeSetting.DISABLED:
                                            if actor.get_naked_type() == WW_SexNakedType.BOTTOM or actor.get_naked_type() == WW_SexNakedType.ALL or actor.get_naked_type() == WW_SexNakedType.FORCE_ALL or undress_setting == WW_SexUndressingTypeSetting.COMPLETE:
                                                self.omutsu_sim.remove_diaper(force_remove=True, update_client=True)






                # apply_outfit_parts_for_diaper_load(self.sim_info)

            except Exception as e:
                logger.error("wicked_whims_stat_watcher failed to run.")
                logger.error(traceback.format_exc())

    def wicked_whims_stat_removed(self, stat_type):
        if stat_type.guid64 == WW_SimStatistic.WW_SEX_ACTIVE_INSTANCE_IDENTIFIER or stat_type.guid64 == WW_SimStatistic.WW_SEX_ACTIVE_INSTANCE_ANIMATION_INDEX or stat_type.guid64 == WW_SimStatistic.WW_IS_SIM_IN_SEX:
            try:
                logger.info("wicked_whims_stat_removed {}".format(stat_type))
                self.value_dict.pop(stat_type.guid64, None)
            except Exception as e:
                logger.error("wicked_whims_stat_removed failed to run.")
                logger.error(traceback.format_exc())

    def on_diaper_load_stat_removed(self, stat):
        # logger.info("stat {}", dir(stat))
        if stat.guid64 == IwnBedwettingStatistic.DIAPER_WETNESS or stat.guid64 == IwnBedwettingStatistic.DIAPER_MESSINESS:
            logger.info("on_diaper_load_stat_removed")
            try:
                self.omutsu_sim.apply_outfit_parts_for_diaper_load()
                self.value_dict.pop(stat.guid64, None)
                # if stat is not None:
                #     logger.info("stat {}", stat)
                #     logger.info("stat {}", stat.__class__)
                #     logger.info("stat {}", dir(stat))
                #     if stat.tracker is not None:
                #         logger.info("stat.tracker {}", stat.tracker)
                #         logger.info("stat.tracker {}", dir(stat.tracker))
                #         if hasattr(stat, 'owner') and stat.tracker.owner is not None:
                #             apply_outfit_parts_for_diaper_load(stat.tracker.owner)
            except Exception as e:
                logger.error("on_diaper_load_stat_removed failed to run.")
                logger.error(traceback.format_exc())


@inject(SimInfo, 'load_sim_info')
def _iwnbedwetting_sim_info_load_sim_info(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        omutsu_sim = OmutsuSim(self)
        # register_on_pre_outfit_change_callback(self, _on_sim_outfit_change)
        omutsu_sim.register_on_outfit_changed_callback(_on_sim_outfit_change)
        omutsu_sim.register_on_buff_added_callback(_on_buff_added)
        # omutsu_sim.register_on_buff_added_callback(_on_buff_added)
        omutsu_sim.register_on_buff_removed_callback(_on_buff_removed)
        add_diaper_load_tracking(self)
        evaluate_buffs(self)
        omutsu_sim.apply_outfit_parts_for_diaper_load()
        if omutsu_sim.outfit_contains_pacifier():
            if not omutsu_sim.has_buff(IwnBedwettingBuff.HAS_PACIFIER):
                omutsu_sim.add_buff(IwnBedwettingBuff.HAS_PACIFIER)
        else:
            if omutsu_sim.has_buff(IwnBedwettingBuff.HAS_PACIFIER):
                omutsu_sim.remove_statistic(IwnBedwettingStatistic.CURRENT_PACIFIER)
                omutsu_sim.remove_buff(IwnBedwettingBuff.HAS_PACIFIER)
    except Exception as ex:
        try:
            logger.error("_iwnbedwetting_sim_info_load_sim_info failed to run.")
            logger.error(traceback.format_exc())
        finally:
            ex = None
            del ex

    return result


def evaluate_buffs(sim_info, update_client=True):
    if sim_info is not None:
        logger.info("evaluate_buffs {}".format(sim_info))
        for buff_type in list(sim_info.get_active_buff_types()):
            _on_buff_added(buff_type, sim_info.id, update_client)


def _on_sim_outfit_change(sim_info, new_outfit, previous_outfit):
    if sim_info is not None:
        # sim_info.unregister_for_outfit_changed_callback(_on_sim_outfit_change)
        try:
            omutsu_sim = OmutsuSim(sim_info)
            logger.info("_on_sim_outfit_change to {} start {}".format(new_outfit, sim_info))
            if omutsu_sim.outfit_contains_pacifier(new_outfit):
                if not omutsu_sim.has_buff(IwnBedwettingBuff.HAS_PACIFIER):
                    omutsu_sim.add_buff(IwnBedwettingBuff.HAS_PACIFIER)
            else:
                if omutsu_sim.has_buff(IwnBedwettingBuff.HAS_PACIFIER):
                    omutsu_sim.remove_statistic(IwnBedwettingStatistic.CURRENT_PACIFIER)
                    omutsu_sim.remove_buff(IwnBedwettingBuff.HAS_PACIFIER)
            if omutsu_sim.have_pants_changed(new_outfit, previous_outfit):
                logger.info("Pants changed")
                omutsu_sim.remove_buff(IwnBedwettingBuff.WET_PANTS_OVERLAY)
                omutsu_sim.remove_buff(IwnBedwettingBuff.WET_CROTCH_OVERLAY)
                omutsu_sim.remove_buff(IwnBedwettingBuff.LEAKY_DIAPER_OVERLAY)
                omutsu_sim.remove_buff(IwnBedwettingBuff.OVERFLOWING_DIAPER_OVERLAY)
            else:
                logger.info("Pants have not changed")

            if omutsu_sim.has_trait(IwnBedwettingTrait.NO_VISIBLE_DIAPERS):
                return

            if new_outfit[0] not in outfit_categories_excluded_from_diaper:
                if omutsu_sim.is_wearing_diaper():
                # if wearing_diaper_item(sim_info.id):
                    if omutsu_sim.is_diaper_accessory_removed(new_outfit, previous_outfit):
                        logger.info("Diaper accessory removed")
                        new_parts = omutsu_sim.get_outfit_parts(new_outfit)
                        diaper_parts = omutsu_sim.get_diaper_parts(previous_outfit,include_bottom=False)
                        for body_type, diaper_part in diaper_parts.items():
                            new_parts[body_type] = diaper_part
                        logger.info("Forcing visible diaper accessory back on {}".format(sim_info))
                        omutsu_sim.set_outfit_parts(new_outfit, new_parts)
                    elif len(omutsu_sim.get_diaper_parts(new_outfit).keys()) == 0:
                        logger.info("{} needs a diaper".format(sim_info))
                        omutsu_sim.put_on_random_diaper_accessory(update_client=True)

            # for callback in sim_info.on_outfit_changed:
            #     logger.info(str(callback.__qualname__))
            evaluate_buffs(sim_info, update_client=True)
            omutsu_sim.apply_outfit_parts_for_diaper_load(update_client=True)
        finally:
            logger.info("_on_sim_outfit_change done {}".format(sim_info))
            # sim_info.register_for_outfit_changed_callback(_on_sim_outfit_change)


@sims4.commands.Command('ccshow', command_type=sims4.commands.CommandType.Live)
def ccshow(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('mod started:')


def _get_statistic_manager():
    return services.get_instance_manager(sims4.resources.Types.STATISTIC)


check_diaper_buffs = {IwnBedwettingBuff.DIAPER_DUMMY_BUFF, NativeBuff.MOOD_HIDDEN_ASLEEP, NativeBuff.SIM_IS_SLEEPING_HIDDEN, NativeBuff.SIM_IS_SLEEPING, IwnBedwettingBuff.MANDATORY_PADDING, IwnBedwettingBuff.TRAIT_DIAPERED_247, IwnBedwettingBuff.TRAIT_DIAPERED_247_MEDICAL, IwnBedwettingBuff.TRAIT_DIAPER_PUNISHED, IwnBedwettingBuff.TRAIT_WEARING_DIAPER_ITEM, IwnBedwettingBuff.TRAIT_NEVER_POTTY_TRAINED, IwnBedwettingBuff.TRAIT_SLEEPS_IN_DIAPERS}


def _on_buff_added(buff_type, sim_id, update_client=True):
    if buff_type is not None:
        if sim_id is not None:
            omutsu_sim = OmutsuSim(sim_id)
            if omutsu_sim.has_trait(IwnBedwettingTrait.NO_VISIBLE_DIAPERS):
                return

            # if not has_buff(10309070037716691412):
            #     remove_diaper(sim_id)

            # if not omutsu_sim.is_wearing_diaper():
            #     remove_diaper(sim_id)
            # logger.info('on_buff_added: {} {}'.format(buff_type, sim_id))
            if buff_type.guid64 in remove_diaper_buffs and not omutsu_sim.is_wearing_diaper():
                remove_diaper(sim_id, update_client)
            else:
                if buff_type.guid64 in force_diaper_pants_buffs:
                    put_on_random_diaper_bottom(sim_id, update_client)
                elif buff_type.guid64 in force_diaper_accessory_buffs:
                    put_on_random_diaper_accessory(sim_id, update_client)
                elif buff_type.guid64 in check_diaper_buffs and omutsu_sim.is_wearing_diaper():
                    put_on_random_diaper_accessory(sim_id, update_client)


def _on_buff_removed(buff_type, sim_id):
    if buff_type is not None:
        if sim_id is not None:
            omutsu_sim = OmutsuSim(sim_id)
            if omutsu_sim.has_trait(IwnBedwettingTrait.NO_VISIBLE_DIAPERS):
                return

            if buff_type.guid64 in check_diaper_buffs and not omutsu_sim.is_wearing_diaper():
                remove_diaper(sim_id)

            if buff_type.guid64 in remove_diaper_buffs and omutsu_sim.is_wearing_diaper():
                # remove_diaper(sim_id)
                put_on_random_diaper_accessory(sim_id)
            # logger.info('on_buff_added: {} {}'.format(buff_type, sim_id))
            if buff_type.guid64 in force_diaper_pants_buffs:
                if not omutsu_sim.is_wearing_diaper():
                    logger.info("Not a diaper wearer")
                    remove_diaper(sim_id)
                else:
                    logger.info("Diaper wearer")
            if buff_type.guid64 in force_diaper_accessory_buffs:
                if not omutsu_sim.is_wearing_diaper():
                    logger.info("Not a diaper wearer")
                    remove_diaper(sim_id)
                else:
                    logger.info("Diaper wearer")


def get_all_buffs():
    buff_manager = services.get_instance_manager(sims4.resources.Types.BUFF)
    return buff_manager.types.values()
    # return [buff_manager.get(129473)]


@inject(InstanceManager, 'load_data_into_class_instances')
def fix_buff_compatibility(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        if self.TYPE != Types.BUFF:
            return result

        logger.info("Injecting buff compatibility")
        affordance_manager = services.affordance_manager()

        for buff in get_all_buffs():
            if not hasattr(buff, 'game_effect_modifier') or not hasattr(buff.game_effect_modifier, '_game_effect_modifiers'):
                continue
            for (index, modifier) in enumerate(buff.game_effect_modifier._game_effect_modifiers):
                if isinstance(modifier, AutonomyModifier):
                    if getattr(modifier, "_suppress_self_affordances", False):
                        if modifier._provided_affordance_compatibility is not None:
                            if hasattr(modifier._provided_affordance_compatibility._tuned_values, 'default_inclusion'):
                                # logger.info('{}'.format(tun.super_affordance_compatibility._tuned_values))
                                if hasattr(modifier._provided_affordance_compatibility._tuned_values.default_inclusion,
                                           'include_all_by_default') and not modifier._provided_affordance_compatibility._tuned_values.default_inclusion.include_all_by_default:

                                    logger.info('  {}: found exclude_all compatibility', buff)

                                    # logger.info('{}'.format(
                                    #     tun.super_affordance_compatibility._tuned_values.default_inclusion.include_affordances))

                                    default_inclusion = dict(modifier._provided_affordance_compatibility._tuned_values.default_inclusion)
                                    affordances = set(modifier._provided_affordance_compatibility._tuned_values.default_inclusion.include_affordances)
                                    for interaction_id in general_diaper_usage_affordances:
                                        tuning_class = affordance_manager.get(interaction_id)
                                        if tuning_class is not None and tuning_class not in affordances:
                                            affordances.add(tuning_class)

                                    default_inclusion['include_affordances'] = frozenset(affordances)
                                    default_inclusion_immutable_slots_cls = sims4.collections.make_immutable_slots_class(
                                        default_inclusion.keys())
                                    default_inclusion_slots = default_inclusion_immutable_slots_cls(default_inclusion)
                                    provided_affordance_compatibility = dict(modifier._provided_affordance_compatibility._tuned_values)
                                    provided_affordance_compatibility['default_inclusion'] = default_inclusion_slots
                                    provided_affordance_compatibility_immutable_slots_cls = sims4.collections.make_immutable_slots_class(
                                        provided_affordance_compatibility.keys())
                                    provided_affordance_compatibility_slots = provided_affordance_compatibility_immutable_slots_cls(
                                        provided_affordance_compatibility)
                                    modifier._provided_affordance_compatibility._tuned_values = provided_affordance_compatibility_slots
    except Exception:
        logger.error("fix_buff_compatibility failed to run.")
        logger.error(traceback.format_exc())
    return result


@sims4.commands.Command('iwn.suck_favorite_pacifier', command_type=sims4.commands.CommandType.Live)
def suck_favorite_pacifier(owner_id:int=None, _connection=None):
    OmutsuSim(owner_id).suck_favorite_pacifier()


@sims4.commands.Command('iwn.suck_random_pacifier', command_type=sims4.commands.CommandType.Live)
def suck_random_pacifier(owner_id:int=None, _connection=None):
    OmutsuSim(owner_id).suck_random_pacifier()


@sims4.commands.Command('iwn.remove_pacifier', command_type=sims4.commands.CommandType.Live)
def remove_pacifier(owner_id:int=None, _connection=None):
    OmutsuSim(owner_id).remove_pacifier()


@sims4.commands.Command('iwn.set_favorite_pacifier', command_type=sims4.commands.CommandType.Live)
def set_favorite_pacifier(owner_id:int=None, _connection=None):
    OmutsuSim(owner_id).set_favorite_pacifier()


@sims4.commands.Command('iwn.diaper_load_changed', command_type=sims4.commands.CommandType.Live)
def diaper_load_changed(owner_id:int=None, _connection=None):
    OmutsuSim(owner_id).apply_outfit_parts_for_diaper_load()


@sims4.commands.Command('iwn.force_into_diaper', command_type=sims4.commands.CommandType.Live)
def force_into_diaper(owner_id:int=None, _connection=None):
    OmutsuSim(owner_id).put_on_random_diaper_bottom(owner_id, _connection, remove_full_body=True, remove_tights=True, update_client=True)


outfit_categories_excluded_from_diaper = [OutfitCategory.SWIMWEAR,OutfitCategory.BATHING,OutfitCategory.SPECIAL]


@sims4.commands.Command('iwn.put_on_random_diaper_bottom', command_type=sims4.commands.CommandType.Live)
def put_on_random_diaper_bottom(owner_id:int=None, object_instance_id=None,  _connection=None, remove_full_body:bool=False, remove_tights:bool=False, remove_top:bool=False, outfit_category_and_index=None, update_client=True):
    if not _ember_detected:
        return
    try:
        OmutsuSim(owner_id).put_on_random_diaper_bottom(object_instance_id, remove_full_body, remove_tights, remove_top, outfit_category_and_index, update_client)
    except Exception as e:
        logger.error("put_on_random_diaper_bottom failed to run.")
        logger.error(traceback.format_exc())


@sims4.commands.Command('iwn.update_default_diaper', command_type=sims4.commands.CommandType.Live)
def update_default_diaper(owner_id:int=None, force_change:bool=False, _connection=None):
    omutsu_sim = OmutsuSim(owner_id)
    if not omutsu_sim.has_trait(IwnBedwettingTrait.NO_VISIBLE_DIAPERS):
        omutsu_sim.put_on_random_diaper_accessory(force_change=True,_connection=_connection)


@sims4.commands.Command('iwn.put_on_random_diaper_accessory', command_type=sims4.commands.CommandType.Live)
def put_on_random_diaper_accessory(owner_id:int=None, object_instance_id=None, _connection=None, outfit_category_and_index=None, update_client=True, force_change=False):
    if not _ember_detected:
        return
    try:
        OmutsuSim(owner_id).put_on_random_diaper_accessory(object_instance_id, outfit_category_and_index, update_client, force_change)
    except Exception as e:
        logger.error("put_on_random_diaper_accessory failed to run.")
        logger.error(traceback.format_exc())

@sims4.commands.Command('iwn.remove_diaper', command_type=sims4.commands.CommandType.Live)
def remove_diaper(owner_id:int=None, _connection=None, force_remove=False, outfit_category_and_index=None, update_client=True):
    # if not _ember_detected:
    #     return
    try:
        OmutsuSim(owner_id).remove_diaper(force_remove, outfit_category_and_index, update_client)
    except Exception as e:
        logger.error("remove_diaper failed to run.")
        logger.error(traceback.format_exc())


def get_statistic_tracker(sim_info, statistic_id):
    if sim_info is not None and statistic_id is not None:
        statistic_instance = _get_statistic_manager().get(statistic_id)
        if statistic_instance is not None:
            if sim_info.has_component(objects.components.types.STATISTIC_COMPONENT):
                statistics_component = sim_info.get_component(objects.components.types.STATISTIC_COMPONENT)
                if statistics_component is not None:
                    return statistics_component.get_tracker(statistic_instance)
    return None


update_check_url = 'http://lilninthel.cc/currentversion.txt'

REQUEST_HEADER = {
  'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
  'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  'Accept-Charset': "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
  'Accept-Encoding': "none",
  'Accept-Language': "en-US,en;q=0.8",
  'Connection': "keep-alive"}

latest_version_string = IWN_BED_WETTING_VERSION


def is_newer_version_available():
    global latest_version_string
    try:
        req = urllib.request.Request(update_check_url, None, REQUEST_HEADER)
        with urllib.request.urlopen(req, timeout=4.0) as response:
            published_version_str = response.read().decode('utf-8').strip()
            if published_version_str:
                p_ver = published_version_str.split('.')
                mod_ver = IWN_BED_WETTING_VERSION.split('.')
                for i in range(len(p_ver)):
                    if int(p_ver[i]) > int(mod_ver[i]):
                        latest_version_string = published_version_str
                        return True
                    if int(p_ver[i]) < int(mod_ver[i]):
                        return False
        return False
    except urllib.error.URLError as e:
        logger.error("check_version failed to run.")
        logger.error(traceback.format_exc())


@sims4.commands.Command('iwn.open_loverslab_club', command_type=sims4.commands.CommandType.Live)
def open_loverslab_club(_connection=None):
    webbrowser.open("https://www.loverslab.com/clubs/9-little-space-private-abdl-mods-and-forums/")
    services.game_clock_service().set_clock_speed(ClockSpeedMode.PAUSED)


@sims4.commands.Command('iwn.open_mod_page', command_type=sims4.commands.CommandType.Live)
def open_mod_page(_connection=None):
    webbrowser.open("https://www.loverslab.com/files/file/28368-iwnbedwetting-extended/")
    services.game_clock_service().set_clock_speed(ClockSpeedMode.PAUSED)


@sims4.commands.Command('iwn.open_ember_mod_page', command_type=sims4.commands.CommandType.Live)
def open_ember_mod_page(_connection=None):
    webbrowser.open("https://www.loverslab.com/files/file/30769-universal-adult-diaper-with-automatic-bulge-and-peek-effects-female-and-male/")
    services.game_clock_service().set_clock_speed(ClockSpeedMode.PAUSED)


@sims4.commands.Command('iwn.set_statistic_value', command_type=sims4.commands.CommandType.Live)
def set_statistic_value(owner_id:int=None, statistic_id=None, new_value=None, _connection=None):
    OmutsuSim(owner_id).set_statistic_value(statistic_id, new_value)


@sims4.commands.Command('iwn.remove_statistic', command_type=sims4.commands.CommandType.Live)
def remove_statistic(owner_id:int=None, statistic_id=None, _connection=None):
    OmutsuSim(owner_id).remove_statistic(statistic_id)


def ShowNotification(title_id, str_id, simdata):
    client = services.client_manager().get_first_client()
    if simdata is None:
        simdata = client.active_sim
    localized_title = lambda**_: sims4.localization._create_localized_string(title_id)
    localized_text = lambda**_: sims4.localization._create_localized_string(str_id)
    notification = UiDialogNotification.TunableFactory().default((client.active_sim), text=localized_text, title=localized_title)
    notification.show_dialog(icon_override=(None, simdata))


def ShowNotificationInternal(title_str, text_str, simdata):
    client = services.client_manager().get_first_client()
    if simdata is None:
        simdata = client.active_sim
    prime_icon = lambda _: IconInfoData(obj_instance=simdata)
    notification = UiDialogNotification.TunableFactory().default((client.active_sim), text=text_str, title=title_str, icon=prime_icon)
    notification.show_dialog()


def DebugNotification(text, title=None):
    client = services.client_manager().get_first_client()
    if client:
        pass
    if client.active_sim:
        if title is None:
            title = 'Debug'
        notification = UiDialogNotification.TunableFactory().default((client.active_sim), text=(lambda**_: LocalizationHelperTuning.get_raw_text(text)
), title=(lambda**_: LocalizationHelperTuning.get_raw_text(title)
))
        notification.show_dialog(icon_override=(None, client.active_sim))


sleeping_diaper_usage_affordances = [DiaperInteraction.PEE, DiaperInteraction.PEE_CONTINUATION, BedwettingInteraction.BEDWET, BedwettingInteraction.BEDWET_CONTINUATION]

general_diaper_usage_affordances = [DiaperInteraction.PEE,
                                    DiaperInteraction.PEE_CONTINUATION,
                                    DiaperInteraction.PEE_IMMEDIATE,
                                    DiaperInteraction.PEE_STANDING,
                                    DiaperInteraction.POOP,
                                    DiaperInteraction.POOP_CONTINUATION,
                                    DiaperInteraction.POOP_IMMEDIATE,
                                    DiaperInteraction.POOP_STANDING,
                                    DiaperInteraction.COMBINED,
                                    DiaperInteraction.COMBINED_CONTINUATION,
                                    DiaperInteraction.COMBINED_IMMEDIATE,
                                    DiaperInteraction.COMBINED_STANDING
                                    ]



@sims4.commands.Command('iwn.play_peeing_sound', command_type=sims4.commands.CommandType.Live)
def play_peeing_sound(owner_id:int=None, duration=5.0, _connection=None):
    try:
        return
        # logger.info("play_peeing_sound")
        # lot_trait_manager = services.get_instance_manager(sims4.resources.Types.ZONE_MODIFIER)
        # lot_trait = lot_trait_manager.get(144143)
        #
        # # logger.info(str(lot_trait.schedule._tuned_values))
        # # logger.info(str(dir(lot_trait.schedule._tuned_values)))
        # action = lot_trait.schedule.schedule_entries[0].actions[0]
        #
        # logger.info(str(action.play_sound))
        # logger.info(str(action.play_sound.sound_effect))
        #
        # sim_info = services.sim_info_manager().get(owner_id)
        # if sim_info is not None:
        #     if owner_id is not None:
        #         affordance_manager = services.affordance_manager()
        #         tun = affordance_manager.get(DiaperInteraction.PEE)
        #
        #         # audio = tun.basic_extras[1].audio_sting
        #         # TunablePlayAudio._factory(sim_info, audio.audio, audio.joint_name_hash, audio.play_on_active_sim_only, audio.immediate_audio)
        #
        #         logger.info(str(tun.basic_extras[1]))
        #         logger.info(str(tun.basic_extras[1].audio_sting))
        #
        #         # start_sound(action.play_sound, duration, sim_info)
        #         start_sound(tun.basic_extras[1], duration, sim_info)
        #         # start_sound(action.play_sound, duration, sim_info)

    except Exception:
        logger.error("play_peeing_sound failed to run.")
        logger.error(traceback.format_exc())


@inject(InstanceManager, 'load_data_into_class_instances')
def modify_sleep_affordances(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        if self.TYPE != Types.INTERACTION:
            return result

        logger.info('Injecting Sleep Affordances')
        bladder_control_test = services.snippet_manager().get(IwnBedwettingTestSet.CAN_CONTROL_BLADDER)


        affordance_manager = services.affordance_manager()

        # tun = affordance_manager.get(DiaperInteraction.PEE)
        #
        # logger.info(str(tun.basic_extras))
        # logger.info(str(dir(tun.basic_extras)))
        # logger.info(str(tun.basic_extras[1]))
        # logger.info(str(dir(tun.basic_extras[1])))
        # logger.info(str(tun.basic_extras[1]._tuned_values))
        # logger.info(str(dir(tun.basic_extras[1]._tuned_values)))
        # logger.info(str(tun.basic_extras[1].audio_sting))
        # logger.info(str(dir(tun.basic_extras[1].audio_sting)))
        # logger.info(str(tun.basic_extras[1].audio_sting.audio))
        # logger.info(str(dir(tun.basic_extras[1].audio_sting.audio)))
        # logger.info(str(tun.basic_extras[1].audio_sting._tuned_values))
        # logger.info(str(dir(tun.basic_extras[1].audio_sting._tuned_values)))
        # logger.info(str(tun.basic_extras[1].audio_sting._tuned_values.audio))
        # logger.info(str(dir(tun.basic_extras[1].audio_sting._tuned_values.audio)))

        # lot_trait_manager = services.get_instance_manager(sims4.resources.Types.ZONE_MODIFIER)
        # lot_trait = lot_trait_manager.get(144143)
        #
        # logger.info(str(lot_trait.schedule._tuned_values))
        # logger.info(str(dir(lot_trait.schedule._tuned_values)))
        # action = lot_trait.schedule.schedule_entries[0].actions[0]
        #
        # logger.info(str(action.play_sound))
        # logger.info(str(dir(action.play_sound)))
        # logger.info(str(action.play_sound.sound_effect))
        # logger.info(str(dir(action.play_sound.sound_effect)))

        for tun in affordance_manager._tuned_classes.values():
            # if hasattr(tun, 'sim_affinity_posture_scoring_data') and tun.sim_affinity_posture_scoring_data is not None:
            if hasattr(tun, 'appropriateness_tags') and tun.appropriateness_tags is not None:
                if Tag.Appropriateness_Sleeping not in tun.appropriateness_tags:
                    continue
                # if InteractionPostureAffinityTag.Sleeping not in tun.sim_affinity_posture_scoring_data.my_tags:
                #     continue
                # if hasattr(tun, '__name__') and ('_Sleep' in tun.__name__ or '_sleep' in tun.__name__ or '_Nap' in tun.__name__ or '_nap' in tun.__name__):
                if hasattr(tun, 'basic_content') and isinstance(tun.basic_content, FlexibleLengthContent):
                    # logger.info('{}'.format(tun.basic_content))
                    # logger.info('{}'.format(dir(tun.basic_content)))
                    if hasattr(tun.basic_content, 'conditional_actions'):
                        # logger.info('{}'.format(tun.basic_content.conditional_actions))
                        for exitCondition in tun.basic_content.conditional_actions:
                            has_bladder = False
                            if isinstance(exitCondition, ExitCondition):
                                for condition in exitCondition.conditions:
                                    if hasattr(condition._tuned_values, 'stat'):
                                        if condition._tuned_values.stat.guid64 == NativeMotive.BLADDER:
                                            has_bladder = True
                                            break
                                if has_bladder:
                                    # logger.info('{}'.format(dir(exitCondition.tests)))
                                    for idx, test_group in enumerate(exitCondition.tests):
                                        # logger.info('{}'.format(y))
                                        # logger.info('{}'.format(dir(y)))
                                        # if not any(hasattr(x, 'guid64') and x.guid64 == bladder_control_test_guid for x in y):
                                        if bladder_control_test not in test_group:
                                            exitCondition.tests[idx] = test_group + (bladder_control_test,)
                                            # logger.info('{}'.format(exitCondition.tests))
                                    # tests = set(exitCondition.tests)

                # logger.info('{}'.format(tun))
                if hasattr(tun, 'super_affordance_compatibility'):
                    # logger.info('{}'.format(tun))
                    if tun.super_affordance_compatibility is not None:
                        # logger.info('{}'.format(tun.super_affordance_compatibility))
                        # logger.info('{}'.format(dir(tun.super_affordance_compatibility._tuned_values)))
                        if hasattr(tun.super_affordance_compatibility._tuned_values, 'default_inclusion'):
                            # logger.info('{}'.format(tun.super_affordance_compatibility._tuned_values))
                            if hasattr(tun.super_affordance_compatibility._tuned_values.default_inclusion,
                                       'include_all_by_default') and not tun.super_affordance_compatibility._tuned_values.default_inclusion.include_all_by_default:

                                logger.info('  {}: found exclude_all compatibility', tun)

                                # logger.info('{}'.format(
                                #     tun.super_affordance_compatibility._tuned_values.default_inclusion.include_affordances))

                                default_inclusion = dict(tun.super_affordance_compatibility._tuned_values.default_inclusion)
                                affordances = set(tun.super_affordance_compatibility._tuned_values.default_inclusion.include_affordances)
                                for interaction_id in sleeping_diaper_usage_affordances:
                                    tuning_class = affordance_manager.get(interaction_id)
                                    if tuning_class is not None and tuning_class not in affordances:
                                        affordances.add(tuning_class)

                                default_inclusion['include_affordances'] = frozenset(affordances)
                                default_inclusion_immutable_slots_cls = sims4.collections.make_immutable_slots_class(
                                    default_inclusion.keys())
                                default_inclusion_slots = default_inclusion_immutable_slots_cls(default_inclusion)
                                provided_affordance_compatibility = dict(tun.super_affordance_compatibility._tuned_values)
                                provided_affordance_compatibility['default_inclusion'] = default_inclusion_slots
                                provided_affordance_compatibility_immutable_slots_cls = sims4.collections.make_immutable_slots_class(
                                    provided_affordance_compatibility.keys())
                                provided_affordance_compatibility_slots = provided_affordance_compatibility_immutable_slots_cls(
                                    provided_affordance_compatibility)
                                tun.super_affordance_compatibility._tuned_values = provided_affordance_compatibility_slots

                                # affordance_manager = services.affordance_manager()
                                # for sa_id in diaper_usage_affordances:
                                #     tuning_class = affordance_manager.get(sa_id)
                                #     if tuning_class is not None:
                                #         include_set.add(tuning_class)
                                #
                                # tun.super_affordance_compatibility._tuned_values.default_inclusion.include_affordances = frozenset(include_set)

                                # logger.info('{}'.format(tun.super_affordance_compatibility._tuned_values.default_inclusion.include_affordances))

        # block_toilet_for_diapered_sims()
    except Exception as e:
        logger.error("InstanceManager.load_data_into_class_instances injection failed to run.")
        logger.error(traceback.format_exc())

    return result


toilet_autonomy_test_id = 14724461213419608835
toilet_poop_autonomy_test_id = 0
toilet_global_test_id = 15481261038742746897
toilet_poop_global_test_id = 10256216486312683154
toilet_bowels_test_id = 7044116528228840097
# can_poop_test_id = 13075969349031789538
loot_diaper_dependence_used_potty_id = 14520123767131912383
loot_pooped = 9942098895842860377
loot_copy_bowels_to_bladder = 16078470156163414351


@inject(InstanceManager, 'load_data_into_class_instances')
def block_toilet_for_diapered_sims(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        if self.TYPE != Types.INTERACTION:
            return result

        logger.info('Injecting Toilet Affordances')

        snippet_manager = services.snippet_manager()
        toilet_autonomy_test = snippet_manager.get(toilet_autonomy_test_id)
        toilet_poop_autonomy_test = snippet_manager.get(toilet_poop_autonomy_test_id)
        toilet_global_test = snippet_manager.get(toilet_global_test_id)
        toilet_poop_global_test = snippet_manager.get(toilet_poop_global_test_id)
        toilet_bowels_test = snippet_manager.get(toilet_bowels_test_id)

        affordance_manager = services.affordance_manager()
        for guid in InteractionSets.TOILET_USE_INTERACTIONS:
            tun = affordance_manager.get(guid)
            if tun is not None:
                logger.info('{}'.format(tun))
                if guid in InteractionSets.TOILET_POOP_INTERACTIONS:
                    logger.info("Toilet poop detected")
                    if hasattr(tun, 'basic_content') and isinstance(tun.basic_content, FlexibleLengthContent):
                        # logger.info('{}'.format(tun.basic_content))
                        # logger.info('{}'.format(dir(tun.basic_content)))
                        if hasattr(tun.basic_content, 'periodic_stat_change'):
                            # logger.info('{}'.format(tun.basic_content.periodic_stat_change._tuned_values))
                            # logger.info('{}'.format(tun.basic_content.periodic_stat_change._tuned_values.__class__))
                            tuned_values = dict(tun.basic_content.periodic_stat_change._tuned_values)
                            #(< StatisticChangeOp <class 'sims4.tuning.instances.commodity_dirtiness'> ParticipantType.Object >, < StatisticChangeOp < class 'sims4.tuning.instances.commodity_dirtiness' > ParticipantType.Object >, < StatisticChangeOp < class 'sims4.tuning.instances.motive_Bladder' > ParticipantType.Actor >, < StatisticChangeOp < class 'sims4.tuning.instances.motive_Bladder' > ParticipantType.Actor >, < StatisticChangeOp < class 'sims4.tuning.instances.motive_Bladder' > ParticipantType.Actor >, < StatisticChangeOp < class 'sims4.tuning.instances.commodity_Motive_HygieneHands' > ParticipantType.Actor >, < StatisticChangeOp < class 'sims4.tuning.instances.motive_Fun' > ParticipantType.Actor >, < StatisticChangeOp < class 'sims4.tuning.instances.commodity_Utilities_Power' > ParticipantType.Lot > )
                            if 'operations' in tuned_values.keys():
                                # logger.info('{}'.format(tuned_values['operations'].__class__))

                                # tuned_values = dict(StatisticChangeOp.TunableFactory().default._tuned_values)
                                # timing = dict(tuned_values['timing'])
                                # timing['timing'] = 'at_end'
                                # timing = dictionary_to_immutable_slots(timing)
                                # tuned_values['timing'] = timing
                                # loot_list = list()
                                # loot_list.append(services.action_manager().get(loot_diaper_dependence_used_potty_id))
                                # if guid in InteractionSets.TOILET_POOP_INTERACTIONS:
                                #     loot_list.append(services.action_manager().get(loot_pooped))
                                # tuned_values['loot_list'] = tuple(loot_list)
                                # immutable_slots_cls = sims4.collections.make_immutable_slots_class(tuned_values.keys())
                                # tuned_values = immutable_slots_cls(tuned_values)
                                # e = TunableFactory.TunableFactoryWr apper(tuned_values, StatisticChangeOp.__name__, StatisticChangeOp)


                                needs_stat = True
                                for op in tuned_values['operations']:
                                    if isinstance(op, StatisticChangeOp):
                                        if op.stat.guid64 == IwnBedwettingStatistic.MOTIVE_BOWELS:
                                            needs_stat = False
                                            break
                                if needs_stat:
                                    bowel_stat = _get_statistic_manager().get(IwnBedwettingStatistic.MOTIVE_BOWELS)
                                    stat_op = StatisticChangeOp(amount=20, stat=bowel_stat, subject=ParticipantType.Actor, exclusive_to_owning_si=True, min_value=200)
                                    operations = list(tuned_values['operations'])
                                    operations.append(stat_op)
                                    tuned_values_cls = make_immutable_slots_class(tuned_values.keys())
                                    tuned_values['operations'] = tuple(operations)
                                    # tun.basic_content.periodic_stat_change._tuned_values = tuned_values_cls(tuned_values)
                                # logger.info('{}'.format(tun.basic_content.periodic_stat_change._tuned_values))


                                # logger.info('{}'.format(tuned_values['operations']))
                                # logger.info('{}'.format(tuned_values['operations'].__class__))
                                #
                                # for operation in tuned_values['operations']:
                                #     logger.info('{}'.format(operation))
                                #     logger.info('{}'.format(operation.__class__))

                        # if hasattr(tun.basic_content, 'conditional_actions'):
                        #     logger.info('{}'.format(tun.basic_content.conditional_actions))
                        #     for exitCondition in tun.basic_content.conditional_actions:
                        #         has_bladder = False
                        #         if isinstance(exitCondition, ExitCondition):
                        #             for condition in exitCondition.conditions:
                        #                 if hasattr(condition._tuned_values, 'stat'):
                        #                     # ImmutableSlots({'absolute': True, 'stat': <class 'sims4.tuning.instances.motive_Bladder'>, 'threshold': <Threshold >= 100.0>, 'who': <ParticipantType.Actor = 1>})
                        #                     if condition._tuned_values.stat.guid64 == NativeMotive.BLADDER:
                        #                         tuned_values = dict(condition._tuned_values)
                        #                         timing = dict(tuned_values['timing'])
                        #                         timing['timing'] = 'at_end'
                        #                         timing = dictionary_to_immutable_slots(timing)
                        #                         logger.info("{}".format(condition._tuned_values))
                        #                         logger.info("{}".format(dir(condition._tuned_values)))
                        #                         has_bladder = True
                        #                         break
                                    # if has_bladder:
                                    #     dict(ExitCondition.TunableFactory().default._tuned_values)
                                    #     break
                                        # logger.info('{}'.format(dir(exitCondition.tests)))
                                        # for idx, test_group in enumerate(exitCondition.tests):
                                        #     # logger.info('{}'.format(y))
                                        #     # logger.info('{}'.format(dir(y)))
                                        #     # if not any(hasattr(x, 'guid64') and x.guid64 == bladder_control_test_guid for x in y):
                                        #     if bladder_control_test not in test_group:
                                        #         exitCondition.tests[idx] = test_group + (bladder_control_test,)
                                        #         # logger.info('{}'.format(exitCondition.tests))
                                        # # tests = set(exitCondition.tests)

                if hasattr(tun, 'test_autonomous') and len(tun.test_autonomous) > 0:
                    # logger.info('{}'.format(tun.test_autonomous))
                    # logger.info('{}'.format(tun.test_autonomous.__class__))
                    for idx, test_group in enumerate(tun.test_autonomous):
                        # logger.info('{}'.format(tun.test_autonomous[idx].__class__))
                        # logger.info('{}'.format(tun.test_autonomous[idx]))
                        if guid in InteractionSets.TOILET_POOP_INTERACTIONS:
                            if toilet_poop_autonomy_test not in test_group:
                                tun.test_autonomous[idx] = test_group + (toilet_poop_autonomy_test,)
                        else:
                            if toilet_autonomy_test not in test_group:
                                tun.test_autonomous[idx] = test_group + (toilet_autonomy_test,)
                            # logger.info('{}'.format(tun.test_autonomous[idx]))
                        # else:
                        #     logger.info('Toilet autonomy already fixed')
                        #     logger.info('{}'.format(tun.test_autonomous[idx]))
                else:
                    tun.test_autonomous = CompoundTestList()
                    # if guid in InteractionSets.TOILET_POOP_INTERACTIONS:
                    #     tun.test_autonomous.append(list((toilet_poop_autonomy_test,)))
                    # else:
                    #     tun.test_autonomous.append(list((toilet_autonomy_test,)))
                    # tun.test_autonomous[0] = (toilet_autonomy_test,)
                    tun.test_autonomous.append((toilet_autonomy_test,))
                    # logger.info('{}'.format(tun.test_autonomous))
                #

                if guid in InteractionSets.TOILET_POOP_INTERACTIONS:
                    test = toilet_poop_global_test
                else:
                    test = toilet_global_test
                if hasattr(tun, 'test_globals'):
                    # logger.info('{}'.format(tun.test_globals.__class__))
                    # logger.info('{}'.format(tun.test_globals))
                    # logger.info('{}'.format(dir(tun.test_globals)))
                    if test not in tun.test_globals:
                        test_list = list(tun.test_globals)
                        test_list.append(test)
                        tun.test_globals = TestList(test_list)
                        # logger.info('{}'.format(tun.test_globals))
                    # else:
                        # logger.info('Toilet global tests already fixed')
                        # logger.info('{}'.format(tun.test_globals))
                else:
                    test_list = list()
                    test_list.append(test)
                    tun.test_globals = TestList(test_list)
                    # logger.info('{}'.format(tun.test_globals))
                    # tun.test_globals.add(toilet_global_test)

                if guid in InteractionSets.TOILET_POOP_INTERACTIONS:
                    # logger.info("Toilet poop detected")
                    if hasattr(tun, 'tests'):
                        test_groups = []
                        for test_group in tun.tests:
                            tests = []
                            for test in test_group:
                                tests.append(test)
                            test_groups.append(tuple(tests))

                        test_groups.append(tuple([toilet_bowels_test]))
                        tun.tests = CompoundTestList(test_groups)

                # if hasattr(tun, 'basic_extras'):
                #     logger.info('{}'.format(tun.basic_extras))
                #     logger.info('{}'.format(tun.basic_extras.__class__))
                #     logger.info('{}'.format(dir(tun.basic_extras)))
                #     basic_extras = list(tun.basic_extras)
                # else:
                #     basic_extras = list()

                tuned_values = dict(LootElement.TunableFactory().default._tuned_values)
                timing = dict(tuned_values['timing'])
                timing['timing'] = 'at_end'
                timing = dictionary_to_immutable_slots(timing)
                tuned_values['timing'] = timing
                loot_list = list()
                loot_list.append(services.action_manager().get(loot_diaper_dependence_used_potty_id))
                if guid in InteractionSets.TOILET_POOP_INTERACTIONS:
                    loot_list.append(services.action_manager().get(loot_pooped))
                tuned_values['loot_list'] = tuple(loot_list)
                immutable_slots_cls = sims4.collections.make_immutable_slots_class(tuned_values.keys())
                tuned_values = immutable_slots_cls(tuned_values)
                e = TunableFactory.TunableFactoryWrapper(tuned_values, LootElement.__name__, LootElement)
                tun.basic_extras = tun.basic_extras + (e,)

                if guid in InteractionSets.TOILET_POOP_INTERACTIONS:
                    tuned_values = dict(LootElement.TunableFactory().default._tuned_values)
                    timing = dict(tuned_values['timing'])
                    timing['timing'] = 'at_beginning'
                    timing = dictionary_to_immutable_slots(timing)
                    tuned_values['timing'] = timing
                    loot_list = list()
                    loot_list.append(services.action_manager().get(loot_copy_bowels_to_bladder))
                    tuned_values['loot_list'] = tuple(loot_list)
                    immutable_slots_cls = sims4.collections.make_immutable_slots_class(tuned_values.keys())
                    tuned_values = immutable_slots_cls(tuned_values)
                    e = TunableFactory.TunableFactoryWrapper(tuned_values, LootElement.__name__, LootElement)
                    tun.basic_extras = (e,) + tun.basic_extras
                    logger.info('{}'.format(tun.basic_extras))


    except Exception as e:
        logger.error("InstanceManager.load_data_into_class_instances injection failed to run.")
        logger.error(traceback.format_exc())

    return result


if _wicked_whims_installed:
    from iwnbedwetting.xml_injector.add_to_tuning import add_super_affordances_to_sims

    @inject(InstanceManager, 'load_data_into_class_instances')
    def inject_ww_interactions(original, self, *args, **kwargs):
        result = original(self, *args, **kwargs)
        try:
            affordance_manager = services.affordance_manager()
            tunings = []
            for guid in InteractionSets.WW_REQUIRED_INTERACTIONS:
                tun = affordance_manager.get(guid)
                if tun is not None:
                    tunings.append(tun)
            add_super_affordances_to_sims(tunings)
        except Exception as e:
            logger.error("InstanceManager.load_data_into_class_instances injection failed to run.")
            logger.error(traceback.format_exc())
        return result


actor_not_diapered_global_test_id = 14313482733996641359

@inject(InstanceManager, 'load_data_into_class_instances')
def block_ww_pee_here_for_diapered_sims(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        if self.TYPE != Types.INTERACTION:
            return result

        logger.info('Injecting WW Pee Here Affordances')

        snippet_manager = services.snippet_manager()
        toilet_global_test = snippet_manager.get(actor_not_diapered_global_test_id)

        affordance_manager = services.affordance_manager()
        for guid in InteractionSets.WW_PEE_HERE_INTERACTIONS:
            tun = affordance_manager.get(guid)
            if tun is not None:
                logger.info('{}'.format(tun))
                if hasattr(tun, 'test_globals'):
                    # logger.info('{}'.format(tun.test_globals.__class__))
                    # logger.info('{}'.format(tun.test_globals))
                    # logger.info('{}'.format(dir(tun.test_globals)))
                    if toilet_global_test not in tun.test_globals:
                        test_list = list(tun.test_globals)
                        test_list.append(toilet_global_test)
                        tun.test_globals = TestList(test_list)
                        # logger.info('{}'.format(tun.test_globals))
                    # else:
                        # logger.info('Toilet global tests already fixed')
                        # logger.info('{}'.format(tun.test_globals))
                else:
                    test_list = list()
                    test_list.append(toilet_global_test)
                    tun.test_globals = TestList(test_list)
                    # logger.info('{}'.format(tun.test_globals))
                    # tun.test_globals.add(toilet_global_test)
    except Exception as e:
        logger.error("InstanceManager.load_data_into_class_instances injection failed to run.")
        logger.error(traceback.format_exc())

    return result


werewolf_mark_interactions = [NativeInteraction.WEREWOLF_ABILITIES_MARK,
                              NativeInteraction.WEREWOLF_ABILITIES_MARK_RALLY,
                              NativeInteraction.WEREWOLF_ABILITIES_MARK_SELF,
                              NativeInteraction.WEREWOLF_TERRAIN_GOHERE_MARK,
                              NativeInteraction.WEREWOLF_TERRAIN_GOHERE_MARK_RALLY]


@inject(InstanceManager, 'load_data_into_class_instances')
def block_werewolf_mark_territory(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        if self.TYPE != Types.INTERACTION:
            return result

        logger.info('Injecting Werewolf Mark Territory Affordances')

        snippet_manager = services.snippet_manager()
        toilet_global_test = snippet_manager.get(actor_not_diapered_global_test_id)

        affordance_manager = services.affordance_manager()
        for guid in werewolf_mark_interactions:
            tun = affordance_manager.get(guid)
            if tun is not None:
                logger.info('{}'.format(tun))
                if hasattr(tun, 'test_globals'):
                    # logger.info('{}'.format(tun.test_globals.__class__))
                    # logger.info('{}'.format(tun.test_globals))
                    # logger.info('{}'.format(dir(tun.test_globals)))
                    if toilet_global_test not in tun.test_globals:
                        test_list = list(tun.test_globals)
                        test_list.append(toilet_global_test)
                        tun.test_globals = TestList(test_list)
                        # logger.info('{}'.format(tun.test_globals))
                    # else:
                        # logger.info('Toilet global tests already fixed')
                        # logger.info('{}'.format(tun.test_globals))
                else:
                    test_list = list()
                    test_list.append(toilet_global_test)
                    tun.test_globals = TestList(test_list)
                    # logger.info('{}'.format(tun.test_globals))
                    # tun.test_globals.add(toilet_global_test)
    except Exception as e:
        logger.error("InstanceManager.load_data_into_class_instances injection failed to run.")
        logger.error(traceback.format_exc())

    return result


@inject(InstanceManager, 'load_data_into_class_instances')
def little_autonomy_fixer(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        if self.TYPE != Types.INTERACTION:
            return result

        logger.info('Injecting Little Autonomy Fixes')

        excluded_interactions = [DiaperChangeInteraction.SI_TOUCHING_CHANGEDIAPER_CHECK,
                                 DiaperChangeInteraction.SI_TOUCHING_CHANGEDIAPER_ASK,
                                 NativeInteraction.TYAE_WATCH_INFANT_AUTONOMOUS,
                                 NativeInteraction.TYAE_CHECKON_INFANT_MINOR,
                                 NativeInteraction.CRIB_SOCIALS_KISSGOODNIGHT_AUTONOMOUS,
                                 NativeInteraction.CRIB_SOCIALS_TELLBEDTIMESTORY_AUTONOMOUS,
                                 NativeInteraction.INFANT_PRESLEEP_CRIB,
                                 NativeInteraction.INFANT_SLEEP_CRIB,
                                 NativeInteraction.INFANT_PRESLEEP_CRIB_NOIDENTITYTEST,
                                 NativeInteraction.SIM_INFANT_CHAT,
                                 NativeInteraction.INFANT_WATCH,
                                 NativeInteraction.INFANT_WATCH_IMMOBILE_INOBJECT,
                                 NativeInteraction.SOCIALSUPERINTERACTION_CARRYPICKUP_SAVETODDLER,
                                 NativeInteraction.PLAYMAT_SOCIALS_WATCHINFANT,
                                 NativeInteraction.PLAYMAT_SOCIALS_PLAYWITHINFANT,
                                 NativeInteraction.PLAYMAT_PLAYWITHTOYS,
                                 NativeInteraction.PLAYMAT_LOOKATTOYS,
                                 NativeInteraction.INFANT_PRESLEEP_PLAYMAT,
                                 NativeInteraction.INFANT_SLEEPNORMAL_PLAYMAT,
                                 NativeInteraction.TYAE_WATCH_TODDLER,
                                 NativeInteraction.TYAE_WATCH_TODDLER_MOTIVEDISTRESS,
                                 NativeInteraction.HIGHCHAIR_GIVEDESSERTAUTONOMOUSLY,
                                 NativeInteraction.HIGHCHAIR_GIVEDRINKAUTONOMOUSLY,
                                 NativeInteraction.HIGHCHAIR_GIVEFOODAUTONOMOUSLY,
                                 NativeInteraction.HIGHCHAIR_NAP,
                                 NativeInteraction.TODDLER_WATCH_THINKING]

        posture_buffs = [NativeBuff.TODDLER_AUTONOMY_MOD_IN_HIGH_CHAIR,
                         NativeBuff.AUTONOMY_MOD_POSTURE_HIGH_CHAIR,
                         NativeBuff.AUTONOMY_MOD_POSTURE_PLAYMAT,
                         NativeBuff.AUTONOMY_MOD_POSTURE_CRIB]

        snippet_manager = services.snippet_manager()

        standard_test = snippet_manager.get(IwnBedwettingTestSet.LITTLE_AUTONOMY_MOD_ACTOR)
        social_test = snippet_manager.get(IwnBedwettingTestSet.LITTLE_AUTONOMY_MOD_TARGETSIM)

        affordance_manager = services.affordance_manager()
        for tun in affordance_manager._tuned_classes.values():
        # for guid in little_autonomy_targets:
        #     tun = affordance_manager.get(guid)

            try:
                if tun is not None:
                    if getattr(tun, 'guid64', 0) in excluded_interactions:
                        logger.info('Skipping {}'.format(tun))
                        continue

                    if not hasattr(tun, "static_commodities_data") or tun.static_commodities_data is None or len(tun.static_commodities_data) == 0:
                        if hasattr(tun, 'allow_autonomous') and not tun.allow_autonomous:
                            # logger.info('Skipping {}'.format(tun))
                            continue
                    # else:
                    #     logger.info('Static commodities')

                    if getattr(tun, 'guid64', 0) in BedwettingInteraction.get_enum_values():
                        # logger.info('Skipping {}'.format(tun))
                        continue

                    if getattr(tun, 'guid64', 0) in InteractionSets.DIAPER_USE_INTERACTIONS:
                        # logger.info('Skipping {}'.format(tun))
                        continue

                    if getattr(tun, 'guid64', 0) in InteractionSets.PANTS_USE_INTERACTIONS:
                        # logger.info('Skipping {}'.format(tun))
                        continue

                    # logger.info('{}'.format(tun))

                    exclude = True

                    if hasattr(tun, 'test_globals'):
                        for test in tun.test_globals:
                            if isinstance(test, BuffTest):
                                if test.whitelist is not None:
                                    # logger.info('{}'.format(test.whitelist))
                                    # logger.info('{}'.format(dir(test.whitelist)))
                                    for buff in test.whitelist:
                                        # logger.info('{}'.format(buff))
                                        # logger.info('{}'.format(dir(buff)))
                                        if buff is not None and getattr(buff, 'guid64', 0) in posture_buffs:
                                            # logger.info('{}'.format(tun))
                                            # logger.info('Do not exclude this interaction')
                                            exclude = False

                    if hasattr(tun, 'tests'):
                        for idx, test_group in enumerate(tun.tests):
                            for test in test_group:
                                if isinstance(test, BuffTest):
                                    if test.whitelist is not None:
                                        # logger.info('{}'.format(test.whitelist))
                                        # logger.info('{}'.format(dir(test.whitelist)))
                                        for buff in test.whitelist:
                                            # logger.info('{}'.format(buff))
                                            # logger.info('{}'.format(dir(buff)))
                                            if buff is not None and getattr(buff, 'guid64', 0) in posture_buffs:
                                                # logger.info('{}'.format(tun))
                                                # logger.info('Do not exclude this interaction')
                                                exclude = False

                    if exclude:
                        logger.info('{}'.format(tun))
                        # logger.info('{}'.format(tun.__class__))
                        # logger.info('{}'.format(dir(tun)))
                        if hasattr(tun, '_social_group_type'):
                            logger.info('Social interaction')
                            add_tests = (standard_test, social_test,)
                        else:
                            add_tests = (standard_test,)
                        if hasattr(tun, 'test_autonomous') and len(tun.test_autonomous) > 0:
                            for idx, test_group in enumerate(tun.test_autonomous):
                                # for little_autonomy_test in little_autonomy_test_instances:
                                    # if little_autonomy_test is not None and little_autonomy_test not in test_group:
                                        # tun.test_autonomous[idx] = test_group + (little_autonomy_test,)
                                        # if tun.guid64 == 30917:
                                tun.test_autonomous[idx] = test_group + add_tests
                        else:
                            tun.test_autonomous = CompoundTestList()
                            # if isinstance(tun, SocialSuperInteraction):
                                # logger.info('Social interaction')
                            tun.test_autonomous.append(add_tests)
                                # tun.test_autonomous[idx] = test_group + (standard_test, social_test,)
                            # else:
                                # tun.test_autonomous.append((standard_test,))
                                # tun.test_autonomous[idx] = test_group + (standard_test,)



            except:
                logger.error(traceback.format_exc())
                continue

    except Exception as e:
        logger.error("little_autonomy_fixer failed to run.")
        logger.error(traceback.format_exc())

    return result


def dictionary_to_immutable_slots(items):
    immutable_slots_cls = sims4.collections.make_immutable_slots_class(items.keys())
    return immutable_slots_cls(items)


def ShowMod():
    global ModHasRun
    if ModHasRun:
        return

    update_available = is_newer_version_available()
    client = services.client_manager().get_first_client()
    urgency = UiDialogNotification.UiDialogNotificationUrgency.DEFAULT
    information_level = UiDialogNotification.UiDialogNotificationLevel.PLAYER
    visual_type = UiDialogNotification.UiDialogNotificationVisualType.INFORMATION
    button_one_text = "Join Little Space Club"
    button_two_text = "Update Mod"

    button1_response_command = make_immutable_slots_class({
        "arguments", "command"})({'arguments': (), 'command': 'iwn.open_loverslab_club'})
    button1_response = UiDialogResponse(dialog_response_id=ButtonType.DIALOG_RESPONSE_OK,
                                        ui_request=UiDialogResponse.UiDialogUiRequest.SEND_COMMAND,
                                        response_command=button1_response_command,
                                        text=(lambda **_: LocalizationHelperTuning.get_raw_text(button_one_text)))

    button2_response_command = make_immutable_slots_class({
        "arguments", "command"})({'arguments': (), 'command': 'iwn.open_mod_page'})
    button2_response = UiDialogResponse(dialog_response_id=ButtonType.DIALOG_RESPONSE_OK,
                                        ui_request=UiDialogResponse.UiDialogUiRequest.SEND_COMMAND,
                                        response_command=button2_response_command,
                                        text=(lambda **_: LocalizationHelperTuning.get_raw_text(button_two_text)))

    ember_mod_response_command = make_immutable_slots_class({
        "arguments", "command"})({'arguments': (), 'command': 'iwn.open_ember_mod_page'})
    ember_mod_response = UiDialogResponse(dialog_response_id=ButtonType.DIALOG_RESPONSE_OK,
                                        ui_request=UiDialogResponse.UiDialogUiRequest.SEND_COMMAND,
                                        response_command=ember_mod_response_command,
                                        text=(lambda **_: LocalizationHelperTuning.get_raw_text("Install Mod")))

    if update_available:
        # localized_title = lambda **_: LocalizationHelperTuning.get_raw_text('NEW VERSION AVAILABLE: IwnBedWetting Extended+')
        information_level = UiDialogNotification.UiDialogNotificationLevel.SIM
        urgency = UiDialogNotification.UiDialogNotificationUrgency.URGENT
        localized_title = lambda **_: LocalizationHelperTuning.get_raw_text('IwnBedWetting Extended+ {0}'.format(IWN_BED_WETTING_VERSION))
        localized_text = lambda **_: LocalizationHelperTuning.get_raw_text("A newer version of IwnBedWetting Extended+ is available. \n\nInstalled version: {0}\nLatest version: {1}\n\nA LoversLab account and free membership in the Little Space club is required to download the latest version. Add a comment to the mod page if you have any questions, issues, or suggestions.".format(IWN_BED_WETTING_VERSION,latest_version_string))
        dialog = UiDialogNotification.TunableFactory().default((client.active_sim),
                                                               text=localized_text,
                                                               title=localized_title,
                                                               urgency=urgency,
                                                               information_level=information_level,
                                                               visual_type=visual_type,
                                                               ui_responses=(
                                                                   button1_response, button2_response))
        dialog.show_dialog()
        # ShowNotificationInternal(localized_title, localized_text, None)
    else:
        # information_level = UiDialogNotification.UiDialogNotificationLevel.SIM
        localized_title = lambda**_: LocalizationHelperTuning.get_raw_text('IWNBedWetting Extended+ {0}'.format(IWN_BED_WETTING_VERSION))
        localized_text = lambda**_: sims4.localization._create_localized_string(387149544)
        ShowNotificationInternal(localized_title, localized_text, None)


    # dialog.show_dialog()

    # mods = get_mods_files_info()
    # dup_file_names = mods[1]
    # old_files = mods[2]
    # mods_dict = mods[3]
    # old_addons = mods[4]

    if not check_package_version():
        # localized_title = lambda **_: LocalizationHelperTuning.get_raw_text('WARNING: IwnBedWetting Extended+ Old Files Detected')
        # localized_text = lambda **_: LocalizationHelperTuning.get_raw_text('Please delete ALL LilNinthel packages EXCEPT for LilNinthel_IWNBedwetting_Extended_Plus.package or the mod may not function correctly')
        # ShowNotificationInternal(localized_title, localized_text, None)
        dialog = UiDialogOk.TunableFactory().default(None)
        dialog.title = lambda **_: LocalizationHelperTuning.get_raw_text('WARNING: IWNBedWetting Extended+ Package Version Mismatch')
        dialog.text = lambda **_: LocalizationHelperTuning.get_raw_text('Your LilNinthel_IWNBedwetting_Extended_Plus.package does not match the script version, please re-install the mod.')
        dialog.show_dialog()

    if _old_mods_detected:
        # localized_title = lambda **_: LocalizationHelperTuning.get_raw_text('WARNING: IwnBedWetting Extended+ Old Files Detected')
        # localized_text = lambda **_: LocalizationHelperTuning.get_raw_text('Please delete ALL LilNinthel packages EXCEPT for LilNinthel_IWNBedwetting_Extended_Plus.package or the mod may not function correctly')
        # ShowNotificationInternal(localized_title, localized_text, None)
        folder_dict = dict()

        dup_arr = []
        for dup in old_files:
            for file_path in mods_dict[dup.lower()]:
                if file_path not in folder_dict.keys():
                    folder_dict[file_path] = []
                folder_dict[file_path].append(dup)

        for key in folder_dict.keys():
            dup_arr.append('\n{}:'.format(key))
            for file_name in folder_dict[key]:
                dup_arr.append(file_name)

        dup_str = '\n'.join(dup_arr)

        dialog = UiDialogOk.TunableFactory().default(None)
        dialog.title = lambda **_: LocalizationHelperTuning.get_raw_text('WARNING: IWNBedWetting Extended+ Old Files Detected')
        dialog.text = lambda **_: LocalizationHelperTuning.get_raw_text('Please delete ALL LilNinthel .package files EXCEPT for LilNinthel_IWNBedwetting_Extended_Plus.package or the mod may not function correctly\n{}'.format(dup_str))
        dialog.show_dialog()

    if _old_addons_detected and not _admin_flag:
        # localized_title = lambda **_: LocalizationHelperTuning.get_raw_text('WARNING: IwnBedWetting Extended+ Old Files Detected')
        # localized_text = lambda **_: LocalizationHelperTuning.get_raw_text('Please delete ALL LilNinthel packages EXCEPT for LilNinthel_IWNBedwetting_Extended_Plus.package or the mod may not function correctly')
        # ShowNotificationInternal(localized_title, localized_text, None)
        folder_dict = dict()

        dup_arr = []
        for dup in old_addons:
            for file_path in mods_dict[dup.lower()]:
                if file_path not in folder_dict.keys():
                    folder_dict[file_path] = []
                folder_dict[file_path].append(dup)

        for key in folder_dict.keys():
            dup_arr.append('\n{}:'.format(key))
            for file_name in folder_dict[key]:
                dup_arr.append(file_name)

        dup_str = '\n'.join(dup_arr)

        dialog = UiDialogOk.TunableFactory().default(None)
        dialog.title = lambda **_: LocalizationHelperTuning.get_raw_text('WARNING: IWNBedWetting Extended+ Old Add-Ons Detected')
        dialog.text = lambda **_: LocalizationHelperTuning.get_raw_text('Please delete ALL previous versions of the following add-ons: Happily Diapered Extended by BabyLola, Unhappily Diapered Extended by Lil Luna, ABDL Extended by mackico, or Happily Messy Extended by DiaperDump. They are all now included with this mod and may cause issues.\n{}'.format(dup_str))
        dialog.show_dialog()

    # if _duplicate_mods:
    #     dup_arr = []
    #     for dup in dup_file_names:
    #         dup_arr.append('\n{}:'.format(dup))
    #         for file_path in mods_dict[dup.lower()]:
    #             dup_arr.append(file_path)
    #
    #     dup_str = '\n'.join(dup_arr)
    #
    #     information_level = UiDialogNotification.UiDialogNotificationLevel.SIM
    #     urgency = UiDialogNotification.UiDialogNotificationUrgency.URGENT
    #     localized_title = lambda **_: LocalizationHelperTuning.get_raw_text('WARNING: Duplicate Package Names Detected')
    #     localized_text = lambda **_: LocalizationHelperTuning.get_raw_text('You have duplicate package names in your mods folder, you may have installed multiple versions of the same mod.\n{0}'.format(dup_str))
    #     dialog = UiDialogNotification.TunableFactory().default((client.active_sim),
    #                                                            text=localized_text,
    #                                                            title=localized_title,
    #                                                            urgency=urgency,
    #                                                            information_level=information_level,
    #                                                            visual_type=visual_type)
    #     dialog.show_dialog()

    if not _ember_detected:
        information_level = UiDialogNotification.UiDialogNotificationLevel.SIM
        urgency = UiDialogNotification.UiDialogNotificationUrgency.URGENT
        localized_title = lambda **_: LocalizationHelperTuning.get_raw_text('WARNING: Universal Diaper Mod Not Installed')
        localized_text = lambda **_: LocalizationHelperTuning.get_raw_text("IWNBedWetting Extended+ requires LittleEmber's Universal Adult Diaper Mod for visible diaper functionality.\n\nA LoversLab account and free membership in the Little Space club is required to download.")
        dialog = UiDialogNotification.TunableFactory().default((client.active_sim),
                                                               text=localized_text,
                                                               title=localized_title,
                                                               urgency=urgency,
                                                               information_level=information_level,
                                                               visual_type=visual_type,
                                                               ui_responses=(
                                                                   button1_response, ember_mod_response))
        dialog.show_dialog()

    # if not _xml_injector_found:
    #     dialog = UiDialogOk.TunableFactory().default(None)
    #     dialog.title = lambda **_: LocalizationHelperTuning.get_raw_text('WARNING: IwnBedWetting Extended+ - XML Injector Not Detected')
    #     dialog.text = lambda **_: LocalizationHelperTuning.get_raw_text('This mod requires XML Injector to function. Please install the latest XML Injector from https://scumbumbomods.com/#/xml-injector/')
    #     dialog.show_dialog()

    logger.info("WickedWhims installed: {}".format(_wicked_whims_installed))

    ModHasRun = True
    # if devMode:
    #     modify_sleep_affordances()


def check_package_version():
    return get_statistics_service().get_initial_statistic_value(IwnBedwettingStatistic.PACKAGE_VERSION) == PACKAGE_VERSION


@inject(Zone, 'on_loading_screen_animation_finished')
def inject_zone_loading(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        ShowMod()
    except Exception as e:
        logger.error("Zone.on_loading_screen_animation_finished injection failed to run.")
        logger.error(traceback.format_exc())

    return result


@inject(ClubRuleCriteriaTrait, '_populate_criteria_info')
def _populate_criteria_info(original, _, criteria_info, trait, *args, **kwargs):
    original(criteria_info, trait, *args, **kwargs)
    try:
        # logger.info(str(trait))
        # logger.info("criteria_info.name: {}", str(criteria_info.name))
        # logger.info("trait.display_name: {}", str(trait.display_name))
        # logger.info("trait.display_name_gender_neutral: {}", str(trait.display_name_gender_neutral))
        if criteria_info.name.hash == 0:
            # logger.info("Missing display_name_gender_neutral found")
            criteria_info.name = sims4.localization._create_localized_string(trait.display_name._string_id)
    except Exception as e:
        logger.error("ClubRuleCriteriaTrait._populate_criteria_info injection failed to run.")
        logger.error(traceback.format_exc())
        # sims4.log.exception("Injection", "ClubRuleCriteriaTrait.populate_possibilities injection failed to run.", exc=e)


@inject(ClubRuleCriteriaTrait, 'populate_possibilities')
def inject_club_traits(original, _, criteria_proto, *args, **kwargs):
    try:
        # logger.info(str(ClubTunables.CLUB_TRAITS))

        # logger.info(str(dir(ClubTunables.CLUB_TRAITS)))

        # logger.info(str(ClubTunables.CLUB_ICONS))
        # logger.info(str(len(ClubTunables.CLUB_ICONS)))
        # logger.info(str(ClubTunables))

        trait_manager = services.get_instance_manager(sims4.resources.Types.TRAIT)

        target_traits = set()
        target_traits.add(IwnBedwettingTrait.INCONTINENCE)
        target_traits.add(IwnBedwettingTrait.BEDWETTER)
        target_traits.add(IwnBedwettingTrait.PANTS_WETTER)
        target_traits.add(IwnBedwettingTrait.PANTS_POOPER)
        target_traits.add(IwnBedwettingTrait.DESPERATION_ENTHUSIAST)
        target_traits.add(IwnBedwettingTrait.TOILET_BAN)
        target_traits.add(IwnBedwettingTrait.DIAPERED_247)
        target_traits.add(IwnBedwettingTrait.DIAPER_CURIOUS)
        target_traits.add(IwnBedwettingTrait.NEVER_POTTY_TRAINED)
        target_traits.add(IwnBedwettingTrait.MACKICO_ABDL)
        target_traits.add(IwnBedwettingTrait.HAPPILY_MESSY)
        target_traits.add(IwnBedwettingTrait.LOVES_DIAPERS)
        target_traits.add(IwnBedwettingTrait.UNHAPPILY_DIAPERED)
        target_traits.add(IwnBedwettingTrait.LITTLE)
        target_traits.add(IwnBedwettingTrait.DIAPER_DEPENDENT)
        target_traits.add(IwnBedwettingTrait.TOTAL_URINARY_INCONTINENCE)
        target_traits.add(IwnBedwettingTrait.DIAPERED_247_MEDICAL)

        traits = {trait_manager.get(trait_id) for trait_id in target_traits}

        # club_icons = set(ClubTunables.CLUB_ICONS)

        # ClubTunables.CLUB_ICONS = frozenset(club_icons)

        #
        for trait in traits:
            if trait is None:
                continue
            club_traits = set(ClubTunables.CLUB_TRAITS)
            club_traits.add(trait)
            ClubTunables.CLUB_TRAITS = frozenset(club_traits)

        # result = original(criteria_proto, *args, **kwargs)
        #
        # return result
        # for trait2 in target_traits2:
        #     with ProtocolBufferRollback(criteria_proto.criteria_infos) as criteria_info:
        #         ClubRuleCriteriaTrait._populate_criteria_info(criteria_info, trait2)
    except Exception as e:
        logger.error("ClubRuleCriteriaTrait.populate_possibilities injection failed to run.")
        logger.error(traceback.format_exc())
        # sims4.log.exception("Injection", "ClubRuleCriteriaTrait.populate_possibilities injection failed to run.", exc=e)

    return original(criteria_proto, *args, **kwargs)


detect_mods()
