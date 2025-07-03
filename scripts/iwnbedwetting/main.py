import sims4.commands, sims4.reload, services, sims4.callback_utils, webbrowser
from event_testing.tests import TunableTestSet, CompoundTestList, TestList
from interactions.base.basic import FlexibleLengthContent
from interactions.base.super_interaction import SuperInteraction
from interactions.utils.interaction_elements import XevtTriggeredElement
from interactions.utils.loot_element import LootElement
from interactions.utils.statistic_element import ExitCondition
from iwnbedwetting.enums.interactions import InteractionSets
import inspect
from clock import ClockSpeedMode
import enum, os, random
from objects.components import component_definition, ComponentContainer
import objects.components.types
from postures.posture_scoring import InteractionPostureAffinityTag
from sims.sim_info import SimInfo
from sims.sim_info_types import Age, Gender, Species
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims4.callback_utils import CallableList
from sims.sim_info_tests import BuffTest, TraitTest, SimInfoTest
from interactions.social.social_super_interaction import SocialSuperInteraction
from sims4.localization import LocalizationHelperTuning
from sims4.resources import Types
from sims4.tuning.tunable import TunableList, TunableFactory
from statistics.statistic_conditions import StatisticCondition
from tag import Tag
from iwnbedwetting.enums.wickedwhims import WW_SimStatistic, WW_NudityReason, WW_SexNakedType, WW_SexUndressingTypeSetting
from ui.ui_dialog_notification import UiDialogNotification
from distributor.shared_messages import IconInfoData
import objects
from iwnbedwetting.native_enums.traits import NativeTrait
from iwnbedwetting.native_enums.buffs import NativeBuff
from zone import Zone
from sims4.collections import make_immutable_slots_class
from types import MappingProxyType
from clubs.club_tuning import ClubRuleCriteriaTrait, ClubTunables
from interactions.utils.adventure import Adventure
from distributor.rollback import ProtocolBufferRollback
from sims4 import resources, collections
from sims4.collections import FrozenAttributeDict
from satisfaction.satisfaction_tracker import SatisfactionTracker
from sims4.tuning.instance_manager import InstanceManager
from iwnbedwetting.utilities.injector import inject
from iwnbedwetting.enums.rewards import IwnBedwettingReward
from iwnbedwetting.enums.traits import IwnBedwettingTrait
from iwnbedwetting.enums.statistics import IwnBedwettingStatistic, DiaperStateStatistics, StatisticSets
from iwnbedwetting.enums.buffs import IwnBedwettingBuff
import sims4.log
import traceback
from sims.outfits.outfit_enums import BodyType, OutfitCategory
from protocolbuffers import S4Common_pb2, Outfits_pb2, PersistenceBlobs_pb2
from sims.outfits.outfit_utils import get_maximum_outfits_for_category, is_sim_info_wearing_all_outfit_parts
from iwnbedwetting.enums.tunable import DiaperWetness, DiaperMessiness
from iwnbedwetting.diaper_cas_part_config.snippet import DiaperLoadCASConfig
from ui.ui_dialog import UiDialogOk, UiDialogResponse, ButtonType, UiDialogStyle, UiDialogBGStyle
import importlib.util
import urllib
import urllib.request
import urllib.error
import urllib.response

IWN_BED_WETTING_VERSION = "2.0.3"
REWARD_BEDWETTER = 11589092927928958152
REWARD_INCONTINENCE = 2926939328826942378
dTittleFull = (265058837, 265058838, 265058839, 323983041, 323983042, 323983043, 269972373,
               269972374, 269972375)
dDialogFull = (579578961, 579578962, 579578963, 323375589, 323375590, 323375591, 58763729,
               58763730, 58763731)
dDprTittle = (4036030530, 4036030530, 4036030530, 4036030530, 4036030530, 4036030530,
              4036030530, 4036030530, 4036030530)
dDprDlg = (4235025683, 4235025683, 4235025683, 3891057783, 3891057783, 3891057783,
           1657824659, 1657824659, 1657824659)
ModHasRun = False
devMode = False
logger = sims4.log.Logger('IWNBedwettingMain')

old_mod_packages = ('LilNinthel_ABDL_Diaper_Change.package','LilNinthel_ABDL_Uppies.package','LilNinthel_Adult_Diaper_Object.package','LilNinthel_Toddler_Social_Animations.package','LilNinthel_UseDiaper_Animations.package')

old_addons = ('Extended BabyLola Happily Diapered','Extended HappilyMessy_DiaperDump','Extended Lil Luna Unhappily Diapered','Extended mackico ABDL')

_old_mods_detected = False
_old_addons_detected = False
_ember_detected = False
_admin_flag = False


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


@inject(SimInfoBaseWrapper, "__init__")
def _lilninthel_on_sim_info_base_wrapper_init(original, self, *args, **kwargs):
    try:
        self.pre_outfit_changed_diaper = CallableList()
    except Exception:
        logger.error("Error _lilninthel_on_sim_info_base_wrapper_init")
        logger.error(traceback.format_exc())
    return original(self, *args, **kwargs)


@inject(SimInfoBaseWrapper, "_set_current_outfit_without_distribution")
def _lilninthel_on_set_current_outfit_without_distribution(original, self, *args, **kwargs):
    try:
        value = args[0]
        old_value = self._base.outfit_type_and_index
        self.pre_outfit_changed_diaper(self, value, old_value)
    except Exception:
        logger.error("Error _lilninthel_on_set_current_outfit_without_distribution")
        logger.error(traceback.format_exc())
    return original(self, *args, **kwargs)


def register_on_pre_outfit_change_callback(sim_info, callback):
    if callback not in sim_info.pre_outfit_changed_diaper:
        sim_info.pre_outfit_changed_diaper.append(callback)


def unregister_on_pre_outfit_change_callback(sim_info, callback):
    if callback in sim_info.pre_outfit_changed_diaper:
        sim_info.pre_outfit_changed_diaper.remove(callback)

def get_mods_files_info():
    global _old_mods_detected
    global _old_addons_detected
    global _admin_flag
    global _ember_detected
    mod_files_names = set()
    duplicated_mod_files_names = set()
    for _, __, files in os.walk(get_sims_mods_directory()):
        for file_name in files:
            if file_name.endswith('.package'):
                if file_name in old_mod_packages:
                    _old_mods_detected = True
                if file_name.startswith('[Ember]') and file_name.endswith('accessory.package'):
                    _ember_detected = True
                for prefix in old_addons:
                    if file_name.startswith(prefix):
                        _old_addons_detected = True
                if file_name == _admin_package:
                    _admin_flag = True
                    logger.info('Admin mode activated')
                if file_name in mod_files_names:
                    duplicated_mod_files_names.add(file_name)
                else:
                    mod_files_names.add(file_name)

    return (
     sorted(mod_files_names), sorted(duplicated_mod_files_names))


def get_sims_documents_directory():
    file_path = os.path.normpath(os.path.dirname(os.path.realpath(__file__))).replace(os.sep, '/')
    lowercase_file_path_segments = file_path.lower().split('/')
    file_path_segments = file_path.split('/')
    root_segment_index = lowercase_file_path_segments.index('mods')
    root_dir = os.sep.join(file_path_segments[:root_segment_index]) + os.sep
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    return root_dir


def get_sims_mods_directory():
    mods_dir_path = '{}Mods{}'.format(get_sims_documents_directory(), os.sep)
    if not os.path.exists(mods_dir_path):
        os.makedirs(mods_dir_path)
    return mods_dir_path


def get_sims_game_directory():
    file_path = os.path.normpath(os.path.dirname(os.path.realpath(enum.__file__))).replace(os.sep, '/')
    file_path_segments = file_path.split('/')
    root_dir = os.sep.join(file_path_segments[:4]) + os.sep
    return root_dir


def register_satisfaction_store_reward(reward_id, cost, award_type=SatisfactionTracker.SatisfactionAwardTypes.TRAIT):
    """
    Register satisfaction store reward of given type.
    This method retains the original classes state and won't conflict when adding multiple of different rewards.
    The 'award_type' keyword is set to 'TRAIT' as an example of what award types are available.
    :param reward_id: int -> id of the reward instance
    :param cost: int -> amount of satisfaction points this reward will cost
    :param award_type: WhimAwardTypes -> award type enum
    """
    instance_manager = services.get_instance_manager(resources.Types.REWARD)
    reward_instance = instance_manager.get(reward_id)
    if reward_instance is not None:
        immutable_slots_class = collections.make_immutable_slots_class(['cost', 'award_type'])
        reward_immutable_slots = immutable_slots_class(dict(cost=cost, award_type=award_type))
        satisfaction_store_items = dict(SatisfactionTracker.SATISFACTION_STORE_ITEMS)
        satisfaction_store_items[reward_instance] = reward_immutable_slots
        SatisfactionTracker.SATISFACTION_STORE_ITEMS = FrozenAttributeDict(satisfaction_store_items)


@inject(InstanceManager, 'load_data_into_class_instances')
def _load_satisfaction_store_rewards(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        if self.TYPE == Types.REWARD:
            logger.info('Registering reward store items')

            register_satisfaction_store_reward(IwnBedwettingReward.BEDWETTER, 100)
            register_satisfaction_store_reward(IwnBedwettingReward.INCONTINENCE, 100)
            register_satisfaction_store_reward(IwnBedwettingReward.DIAPER_CURIOUS, 100)
            register_satisfaction_store_reward(IwnBedwettingReward.PANTS_WETTER, 100)
            register_satisfaction_store_reward(IwnBedwettingReward.PANTS_POOPER, 100)
            register_satisfaction_store_reward(IwnBedwettingReward.DESPERATION_ENTHUSIAST, 100)
            register_satisfaction_store_reward(IwnBedwettingReward.LITTLE, 100)
            register_satisfaction_store_reward(IwnBedwettingReward.TOILET_BAN, 100)
            register_satisfaction_store_reward(IwnBedwettingReward.DIAPER_DEPENDENT, 100)
            register_satisfaction_store_reward(IwnBedwettingReward.DIAPERED_247, 100)
            register_satisfaction_store_reward(IwnBedwettingReward.UNIVERSAL_CAREGIVER, 100)

    except Exception as e:
        logger.error("InstanceManager.load_data_into_class_instances injection failed to run.")
        logger.error(traceback.format_exc())

    return result


bedwetter_obj_affordance_ids = (7158177636850136246, )
bedwetter_obj_ids = (36433, )
bedwetter_obj_names = ('dresser', )

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

diaper_wetness_stats = [17047720970454098230,]

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

class DiaperWatcherWrapper():
    def __init__(self, sim_info):
        self.sim_info = sim_info
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
                apply_outfit_parts_for_diaper_load(self.sim_info)
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
                set_statistic_value(self.sim_info.id, IwnBedwettingStatistic.DIAPER_TRAINING_SKILL, 100 + new_value*51.8)

    def wicked_whims_stat_watcher(self, stat_type, old_value, new_value):
        if stat_type.guid64 == WW_SimStatistic.WW_SEX_ACTIVE_INSTANCE_IDENTIFIER or stat_type.guid64 == WW_SimStatistic.WW_SEX_ACTIVE_INSTANCE_ANIMATION_INDEX or stat_type.guid64 == WW_SimStatistic.WW_IS_SIM_IN_SEX:
            try:
                logger.info("wicked_whims_stat_watcher {}".format(stat_type))
                if stat_type.guid64 in self.value_dict:
                    logger.info("old {} new {}".format(self.value_dict[stat_type.guid64], new_value))
                    if self.value_dict[stat_type.guid64] == new_value:
                        logger.info("No change in value")
                        return

                active_sex_id = get_statistic_value(self.sim_info, WW_SimStatistic.WW_SEX_ACTIVE_INSTANCE_IDENTIFIER) or 0
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
                                    if sim_id == self.sim_info.id:
                                        # logger.info(str(actor))
                                        # if not has_trait(self.get_sim_id(), visible_diapers_opt_out_trait):
                                        undress_setting = get_sex_setting(SexSetting.SEX_UNDRESSING_TYPE)
                                        npc_undress_setting = get_sex_setting(SexSetting.NPC_SEX_UNDRESSING_TYPE)
                                        # is_npc_only = kwargs.get("is_npc_only", False)
                                        if self.sim_info.is_npc:
                                            undress_setting = npc_undress_setting
                                        if undress_setting != WW_SexUndressingTypeSetting.DISABLED:
                                            if actor.get_naked_type() == WW_SexNakedType.BOTTOM or actor.get_naked_type() == WW_SexNakedType.ALL or actor.get_naked_type() == WW_SexNakedType.FORCE_ALL or undress_setting == WW_SexUndressingTypeSetting.COMPLETE:
                                                remove_diaper(self.sim_info.id, force_remove=True, update_client=True)






                # apply_outfit_parts_for_diaper_load(self.sim_info)
                self.value_dict[stat_type.guid64] = new_value
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
                apply_outfit_parts_for_diaper_load(self.sim_info)
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
        # register_on_pre_outfit_change_callback(self, _on_sim_outfit_change)
        self.register_for_outfit_changed_callback(_on_sim_outfit_change)
        register_on_buff_added_callback(self,_on_buff_added)
        register_on_buff_removed_callback(self,_on_buff_removed)
        add_diaper_load_tracking(self)
        evaluate_buffs(self)
        apply_outfit_parts_for_diaper_load(self)
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


def register_on_buff_added_callback(sim_info, callback):
    if sim_info is not None:
        buff_component = sim_info.Buffs
        if buff_component:
            if callback not in buff_component.on_buff_added:
                buff_component.on_buff_added.append(callback)


def unregister_on_buff_added_callback(sim_info, callback):
    if sim_info is not None:
        buff_component = sim_info.Buffs
        if buff_component:
            if callback in buff_component.on_buff_added:
                buff_component.on_buff_added.remove(callback)


def register_on_buff_removed_callback(sim_info, callback):
    if sim_info is not None:
        buff_component = sim_info.Buffs
        if buff_component:
            if callback not in buff_component.on_buff_removed:
                buff_component.on_buff_removed.append(callback)


def unregister_on_buff_removed_callback(sim_info, callback):
    if sim_info is not None:
        buff_component = sim_info.Buffs
        if buff_component:
            if callback in buff_component.on_buff_removed:
                buff_component.on_buff_removed.remove(callback)


def _on_sim_outfit_change(sim_info, new_outfit, previous_outfit):
    if sim_info is not None:
        # sim_info.unregister_for_outfit_changed_callback(_on_sim_outfit_change)
        try:
            logger.info("_on_sim_outfit_change to {} start {}".format(new_outfit, sim_info))
            if have_pants_changed(sim_info, new_outfit, previous_outfit):
                logger.info("Pants changed")
                remove_buff(sim_info, IwnBedwettingBuff.WET_PANTS_OVERLAY)
                remove_buff(sim_info, IwnBedwettingBuff.WET_CROTCH_OVERLAY)
                remove_buff(sim_info, IwnBedwettingBuff.LEAKY_DIAPER_OVERLAY)
                remove_buff(sim_info, IwnBedwettingBuff.OVERFLOWING_DIAPER_OVERLAY)
            else:
                logger.info("Pants have not changed")

            if has_trait(sim_info.id, visible_diapers_opt_out_trait):
                return

            if new_outfit[0] not in outfit_categories_excluded_from_diaper:
                if is_wearing_diaper(sim_info.id):
                # if wearing_diaper_item(sim_info.id):
                    if is_diaper_accessory_removed(sim_info, new_outfit, previous_outfit):
                        logger.info("Diaper accessory removed")
                        new_parts = get_outfit_parts(sim_info, new_outfit)
                        diaper_parts = get_diaper_parts(get_outfit_parts(sim_info, previous_outfit),include_bottom=False)
                        for body_type, diaper_part in diaper_parts.items():
                            new_parts[body_type] = diaper_part
                        logger.info("Forcing visible diaper accessory back on {}".format(sim_info))
                        set_outfit_parts(sim_info, new_outfit, new_parts)
                    elif len(get_diaper_parts(get_outfit_parts(sim_info, new_outfit)).keys()) == 0:
                        logger.info("{} needs a diaper".format(sim_info))
                        put_on_random_diaper_accessory(sim_info.id, update_client=True)
            # else:
            #     if _wicked_whims_installed:
            #         turbo_sim = TurboSim(sim_info.id)
            #         if turbo_sim is not None:
            #             if is_sim_going_to_sex_interaction(turbo_sim) or is_sim_in_sex_interaction(turbo_sim):
            #             # nudity_reason = get_statistic_value(sim_info, WickedWhimsSimStatistic.WW_NUDITY_REASON)
            #             # if nudity_reason == WickedWhimsNudityReason.SEX:
            #             # (turbo_sim: turbolib2.wrappers.sim.sim.TurboSim, strip_type_top= < StripType.NONE = 0 >,
            #             # strip_type_bottom= < StripType.NONE = 0 >, strip_body_type=-1, save_original=True,
            #             # change_outfit=True, outfit_category_and_index=( < TurboOutfitCategory.SPECIAL = 8 >, 0),
            #             # allow_stripping_gloves = None, allow_stripping_feet = None, allow_stripping_socks = None,
            #             # allow_stripping_leggings = None, nudity_reason = None)
            #             #
            #                 if len(get_diaper_parts(get_outfit_parts(sim_info, new_outfit)).keys()) == 0:
            #                     # strip_outfit(turbo_sim, outfit_category_and_index=new_outfit, strip_body_type=BodyType.INDEX_FINGER_LEFT)
            #                     # logger.info("Sim is undressed for sex, removing diaper")
            #                     # remove_diaper(sim_info, True)
            #                     return
            #             else:
            #             # elif nudity_reason == WickedWhimsNudityReason.POST_SEX:
            #                 if wearing_diaper_item(sim_info.id) or always_wears_diapers(sim_info.id):
            #                     if len(get_diaper_parts(get_outfit_parts(sim_info, new_outfit)).keys()) == 0:
            #                         if not has_trait(sim_info.id, visible_diapers_opt_out_trait):
            #                             logger.info("Sim is dressing up after sex, adding diaper")
            #                             logger.info("{} needs a diaper".format(sim_info))
            #                             put_on_random_diaper_accessory(sim_info.id)

            # for callback in sim_info.on_outfit_changed:
            #     logger.info(str(callback.__qualname__))
            evaluate_buffs(sim_info, update_client=True)
            apply_outfit_parts_for_diaper_load(sim_info, update_client=True)
        finally:
            logger.info("_on_sim_outfit_change done {}".format(sim_info))
            # sim_info.register_for_outfit_changed_callback(_on_sim_outfit_change)


# @inject(objects.game_object.GameObject, 'on_add')
def bedwetter_add_super_affordances_objects(original, self):
    result = original(self)
    try:
        if hasattr(self, 'guid64') is False:
            return
        fcount = 0
        for currName in bedwetter_obj_names:
            if currName in type(self).__name__:
                fcount = fcount + 1

        if fcount < 1:
            return
        sa_list = []
        affordance_manager = services.affordance_manager()
        for sa_id in bedwetter_obj_affordance_ids:
            tuning_class = affordance_manager.get(sa_id)
            if tuning_class is not None:
                sa_list.append(tuning_class)
                logger.info('{} {} {}'.format(self.guid64, type(self).__name__, type(self).__class__.__name__))
                logger.info('Found it and added magic!')

        self._super_affordances = self._super_affordances + tuple(sa_list)
    except Exception as e:
        logger.error("GameObject.on_add injection failed to run.")
        logger.error(traceback.format_exc())

    return result


@sims4.commands.Command('ccshow', command_type=(sims4.commands.CommandType.Live))
def ccshow(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('mod started:')


def _get_statistic_manager():
    return services.get_instance_manager(sims4.resources.Types.STATISTIC)


def _filter_value(value):
    try:
        return float(value)
    except ValueError:
        pass

    return int(value)


EMPTY_DICT = MappingProxyType({})


def get_sim_info_base(sim_info):
    if sim_info is not None and sim_info._base is not None:
        return sim_info._base


# def get_outfit_parts(sim_info, outfit_category_and_index):
#     sim_info = sim_info
#     outfit_data = sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])
#     if outfit_data is None:
#         return EMPTY_DICT
#     outfit_id = getattr(sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1]), 'outfit_id', 0)
#     outfits_msg = sim_info.save_outfits()
#     # logger.info('get_outfit_parts outfits_msg {}', outfits_msg)
#     outfit_data = next(iter((outfit for outfit in outfits_msg.outfits if outfit.category == outfit_category_and_index[0] and outfit.outfit_id == outfit_id)), None)
#     # logger.info('get_outfit_parts outfit_data {}', outfit_data)
#     if outfit_data is None:
#         return EMPTY_DICT
#     body_types = list(outfit_data.body_types_list.body_types)
#     cas_parts = list(outfit_data.parts.ids)
#     color_shifts = list(outfit_data.part_shifts.color_shift)
#     outfit_parts = {}
#     for (i, body_type) in enumerate(body_types):
#         outfit_parts[body_type] = CasPart((cas_parts[i]), color_shift=(color_shifts[i]))
#     return outfit_parts

def get_outfit_parts(sim_info, outfit_category_and_index):
    # sim_info = self.get_sim_info_base() or self.get_sim_info()
    outfit_data = sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])
    if outfit_data is None:
        return EMPTY_DICT
    outfit_id = getattr(sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1]), 'outfit_id', 0)
    outfits_msg = sim_info.save_outfits()
    # outfit_data_msg = next(iter((outfit for outfit in outfits_msg.outfits)), None)
    # if outfit_data_msg is None:
    #     outfit_data_msg = next(iter((outfit for outfit in outfits_msg.outfits)), None)
    # if outfit_data_msg is None:
    #     return EMPTY_DICT
    outfit_data = next(iter((outfit for outfit in outfits_msg.outfits if outfit.category == outfit_category_and_index[0] and outfit.outfit_id == outfit_id)), None)
    # logger.info('get_outfit_parts outfit_data {}', outfit_data)
    if outfit_data is None:
        return EMPTY_DICT
    body_types = list(outfit_data.body_types_list.body_types)
    cas_parts = list(outfit_data.parts.ids)
    color_shifts = list(outfit_data.part_shifts.color_shift)
    object_ids = list(outfit_data.object_ids.object_id)
    layer_ids = list(outfit_data.layer_ids.layer_id)
    outfit_parts = {}
    for (i, body_type) in enumerate(body_types):
        cas_part = CasPart((cas_parts[i]), (color_shifts[i]), (object_ids[i]), (layer_ids[i]))
        if body_type not in outfit_parts:
            outfit_parts[body_type] = (cas_part,)
        else:
            if not isinstance(outfit_parts[body_type], tuple):
                outfit_parts[body_type] = (
                 outfit_parts[body_type],)
            outfit_parts[body_type] += (cas_part,)

    return outfit_parts


def _get_outfit_verification_identifier(body_types, cas_part_ids, color_shifts):
    return frozenset([*body_types, *cas_part_ids, *color_shifts])


# def get_appearance_modifiers_outfit_parts(sim_info, outfit_category_and_index):
#     sim_info_base_wrapper = sim_info.appearance_tracker.appearance_override_sim_info
#     if sim_info_base_wrapper is None:
#         return EMPTY_DICT
#     outfit_data = sim_info_base_wrapper.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])
#     outfit_id = getattr(sim_info_base_wrapper.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1]), 'outfit_id', 0)
#     if outfit_data is None:
#         return EMPTY_DICT
#     outfits_msg = sim_info_base_wrapper.save_outfits()
#     outfit_data = next(iter((outfit for outfit in outfits_msg.outfits if outfit.category == outfit_category_and_index[0] and outfit.outfit_id == outfit_id)), None)
#     if outfit_data is None:
#         return EMPTY_DICT
#     body_types = list(outfit_data.body_types_list.body_types)
#     cas_parts = list(outfit_data.parts.ids)
#     color_shifts = list(outfit_data.part_shifts.color_shift)
#     object_ids = list(outfit_data.object_ids.object_id)
#     layer_ids = list(outfit_data.layer_ids.layer_id)
#     outfit_parts = {}
#     for (i, body_type) in enumerate(body_types):
#         outfit_parts[body_type] = CasPart((cas_parts[i]), (color_shifts[i]), (object_ids[i]), (layer_ids[i]))
#
#     return outfit_parts


force_diaper_pants_buffs = []
force_diaper_accessory_buffs = [IwnBedwettingBuff.MANDATORY_PADDING]

remove_diaper_buffs = [NativeBuff.POOLS_HYGIENE,NativeBuff.SIMIS_SWIMMING,NativeBuff.SIM_IS_IN_BATH]

visible_diapers_opt_out_trait = 12749121714103691140

def is_wearing_diaper(owner_id):
    if owner_id is not None:
        sim_info = services.sim_info_manager().get(owner_id)
        if sim_info is not None:
            current_outfit = sim_info.get_current_outfit()
            if current_outfit is not None and current_outfit[0] == OutfitCategory.BATHING:
                return False

            if has_buff(IwnBedwettingBuff.MANDATORY_PADDING):
                return True

            for buff in remove_diaper_buffs:
                if has_buff(owner_id, buff):
                    return False

            wetness = get_statistic_value(sim_info, IwnBedwettingStatistic.DIAPER_WETNESS) or 0
            messiness = get_statistic_value(sim_info, IwnBedwettingStatistic.DIAPER_WETNESS) or 0

            if wetness > 0 or messiness > 0:
                return True

            if has_trait(owner_id, IwnBedwettingTrait.SLEEPS_IN_DIAPERS) and (has_buff(owner_id, NativeBuff.MOOD_HIDDEN_ASLEEP) or has_buff(owner_id, NativeBuff.SIM_IS_SLEEPING) or has_buff(owner_id, NativeBuff.SIM_IS_SLEEPING_HIDDEN)):
                return True

            if always_wears_diapers(owner_id):
                return True
            if wearing_diaper_item(owner_id):
                return True

    return False

def always_wears_diapers(owner_id):
    if has_trait(owner_id, IwnBedwettingTrait.NEVER_POTTY_TRAINED, IwnBedwettingTrait.DIAPERED_247, IwnBedwettingTrait.DIAPERED_247_MEDICAL, IwnBedwettingTrait.DIAPER_PUNISHED):
        return True
    return False


def wearing_diaper_item(owner_id):
    return has_trait(owner_id, IwnBedwettingTrait.WEARING_DIAPER_ITEM)


def has_buff(owner_id, *buff_ids):
    if owner_id is not None:
        sim_info = services.sim_info_manager().get(owner_id)
        if sim_info is not None:

            sim_buff_ids = {getattr(buff_entry, 'guid64', 0) for buff_entry in sim_info.Buffs}
            return not set(buff_ids).isdisjoint(sim_buff_ids)
            # return sim_info.Buffs.has_buff(buff_type)
            # buff_manager = services.get_instance_manager(sims4.resources.Types.BUFF)
            # buff_instance = buff_manager.get(buff_type)
            # if buff_instance is not None:
            #     return buff_instance in sim_info.get_active_buff_types()
    return False


def has_trait(owner_id, *trait_ids):
    if owner_id is not None:
        sim_info = services.sim_info_manager().get(owner_id)
        if sim_info is not None:
            sim_trait_ids = {trait.guid64 for trait in sim_info.get_traits()}
            return not set(trait_ids).isdisjoint(sim_trait_ids)
    return False


check_diaper_buffs = [IwnBedwettingBuff.DIAPER_DUMMY_BUFF, NativeBuff.MOOD_HIDDEN_ASLEEP, NativeBuff.SIM_IS_SLEEPING_HIDDEN, NativeBuff.SIM_IS_SLEEPING, IwnBedwettingBuff.MANDATORY_PADDING, IwnBedwettingBuff.TRAIT_DIAPERED_247, IwnBedwettingBuff.TRAIT_DIAPERED_247_MEDICAL, IwnBedwettingBuff.TRAIT_DIAPER_PUNISHED, IwnBedwettingBuff.TRAIT_WEARING_DIAPER_ITEM, IwnBedwettingBuff.TRAIT_NEVER_POTTY_TRAINED, IwnBedwettingBuff.TRAIT_SLEEPS_IN_DIAPERS]

def _on_buff_added(buff_type, sim_id, update_client=True):
    if buff_type is not None:
        if sim_id is not None:
            if has_trait(sim_id, visible_diapers_opt_out_trait):
                return

            # if not has_buff(10309070037716691412):
            #     remove_diaper(sim_id)

            # if not is_wearing_diaper(sim_id):
            #     remove_diaper(sim_id)
            # logger.info('on_buff_added: {} {}'.format(buff_type, sim_id))
            if buff_type.guid64 in remove_diaper_buffs and not is_wearing_diaper(sim_id):
                remove_diaper(sim_id, update_client)
            else:
                if buff_type.guid64 in force_diaper_pants_buffs:
                    put_on_random_diaper_bottom(sim_id, update_client)
                elif buff_type.guid64 in force_diaper_accessory_buffs:
                    put_on_random_diaper_accessory(sim_id, update_client)
                elif buff_type.guid64 in check_diaper_buffs and is_wearing_diaper(sim_id):
                    put_on_random_diaper_accessory(sim_id, update_client)


def _on_buff_removed(buff_type, sim_id):
    if buff_type is not None:
        if sim_id is not None:
            if has_trait(sim_id, visible_diapers_opt_out_trait):
                return

            if buff_type.guid64 in check_diaper_buffs and not is_wearing_diaper(sim_id):
                remove_diaper(sim_id)

            if buff_type.guid64 in remove_diaper_buffs and is_wearing_diaper(sim_id):
                # remove_diaper(sim_id)
                put_on_random_diaper_accessory(sim_id)
            # logger.info('on_buff_added: {} {}'.format(buff_type, sim_id))
            if buff_type.guid64 in force_diaper_pants_buffs:
                if not is_wearing_diaper(sim_id):
                    logger.info("Not a diaper wearer")
                    remove_diaper(sim_id)
                else:
                    logger.info("Diaper wearer")
            if buff_type.guid64 in force_diaper_accessory_buffs:
                if not is_wearing_diaper(sim_id):
                    logger.info("Not a diaper wearer")
                    remove_diaper(sim_id)
                else:
                    logger.info("Diaper wearer")


def add_buff(sim_info, buff_id, buff_reason=None):
    buff_manager = services.get_instance_manager(sims4.resources.Types.BUFF)
    buff_instance = buff_manager.get(buff_id)
    if buff_instance is None:
        return False
    if buff_instance in sim_info.get_active_buff_types():
        return False
    # if buff_reason is not None:
    #     buff_reason = LocalizationHelperTuning.get_localized_string(buff_reason)
    return sim_info.add_buff_from_op(buff_instance, buff_reason=buff_reason)


def remove_buff(sim_info, *buff_ids):
    buff_component = sim_info.Buffs
    if not buff_component:
        return False
    buff_ids = set(buff_ids)
    buff_entries = [buff_entry for buff_entry in buff_component if getattr(buff_entry, 'guid64', 0) in buff_ids]
    for buff_entry in buff_entries:
        sim_info.remove_buff_entry(buff_entry)
    return True


@sims4.commands.Command('iwn.diaper_load_changed', command_type=(sims4.commands.CommandType.Live))
def diaper_load_changed(owner_id:int=None, _connection=None):
    if owner_id is not None:
        sim_info = services.sim_info_manager().get(owner_id)
        if sim_info is not None:
            apply_outfit_parts_for_diaper_load(sim_info)


_male_bottom = [11509986916541151536,14935196131981263092,9263557843126228615,17116738985650124656,11377714707345239857,11050266238630918155,18109847548095664823,14529822570535928302,15862920524777542351,12592391533832786983,14530773083303507666]
_male_accessory = [15024033459415991799,10626761853771937099,14604802740542491578,11579388597978100234,10828777962635164723,13099465542238001347,16477299403392253060,11301312599355066913,10518520436121252549,17115575128165822309,17109339264598132275]
_female_bottom = [11276491982480170579,9323691022453188679,11377714707345239857,11798765533300344227,18308005185402329887,15102817938559141327,14134628814573739421,15119513609445981861,17192211726903388244,14847364933606234717,15858575318118471992]
_female_accessory = [17185900473586388270,15174586519016046818,15395696484973795175,14081768220370047012,10702638174933037029,11840689655989022495,14014837071704813112,15880507622158690423,18111581372537224927,11649414196269637966,16423671842319494793]
_child_bottom = [17916267921504688060]
_child_accessory = [16089036029714611952]


@sims4.commands.Command('iwn.force_into_diaper', command_type=(sims4.commands.CommandType.Live))
def force_into_diaper(owner_id:int=None, _connection=None):
    put_on_random_diaper_bottom(owner_id, _connection, remove_full_body=True, remove_tights=True, update_client=True)

outfit_categories_excluded_from_diaper = [OutfitCategory.SWIMWEAR,OutfitCategory.BATHING,OutfitCategory.SPECIAL]


@sims4.commands.Command('iwn.put_on_random_diaper_bottom', command_type=(sims4.commands.CommandType.Live))
def put_on_random_diaper_bottom(owner_id:int=None, _connection=None, remove_full_body:bool=False, remove_tights:bool=False, remove_top:bool=False, outfit_category_and_index=None, update_client=True):
    if not _ember_detected:
        return
    try:
        if owner_id is not None:
            sim_info = services.sim_info_manager().get(owner_id)
            if sim_info is not None:
                if sim_info.species != Species.HUMAN:
                    return
                logger.info("iwn.put_on_random_diaper_bottom: {}", sim_info)
                if outfit_category_and_index is None:
                    outfit_category_and_index = sim_info.get_current_outfit()
                if outfit_category_and_index is not None:
                    if outfit_category_and_index[0] in outfit_categories_excluded_from_diaper:
                        return
                    # logger.info('current_outfit: {}'.format(current_outfit))
                    outfit_parts = get_outfit_parts(sim_info, outfit_category_and_index)
                    if outfit_parts is not None:

                        if remove_full_body:
                            outfit_parts.pop(BodyType.FULL_BODY, None)

                        if remove_tights:
                            outfit_parts.pop(BodyType.TIGHTS, None)

                        if remove_top:
                            outfit_parts.pop(BodyType.UPPER_BODY, None)

                        if BodyType.FULL_BODY in outfit_parts.keys():
                            put_on_random_diaper_accessory(owner_id, _connection)
                            return

                        if BodyType.LOWER_BODY in outfit_parts.keys():
                            for outfit_part in outfit_parts[BodyType.LOWER_BODY]:
                                if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                                    return
                        else:
                            outfit_parts[BodyType.LOWER_BODY] = (CasPart((0)),)

                        diaper_part_id = None
                        if has_trait(sim_info.id, NativeTrait.GENDER_OPTIONS_FRAME_MASCULINE):
                            diaper_part_id = random.choice(
                                DiaperLoadCASConfig.get_default_diaper_parts_ids_for_body_type(BodyType.LOWER_BODY,
                                                                                               _male_bottom))
                        elif has_trait(sim_info.id, NativeTrait.GENDER_OPTIONS_FRAME_FEMININE):
                            diaper_part_id = random.choice(
                                DiaperLoadCASConfig.get_default_diaper_parts_ids_for_body_type(BodyType.LOWER_BODY,
                                                                                               _female_bottom))
                        if diaper_part_id is not None:
                            if sim_info.age in (Age.TEEN, Age.YOUNGADULT, Age.ADULT, Age.ELDER):
                                outfit_parts[BodyType.LOWER_BODY] = (CasPart((diaper_part_id)),)
                                outfit_parts.pop(BodyType.INDEX_FINGER_LEFT, None)
                            elif _admin_flag and sim_info.age == Age.CHILD:
                                outfit_parts[BodyType.LOWER_BODY] = (CasPart((17916267921504688060)),)
                            set_outfit_parts(sim_info, outfit_category_and_index, outfit_parts, update_client)
    except Exception as e:
        logger.error("put_on_random_diaper_bottom failed to run.")
        logger.error(traceback.format_exc())


@sims4.commands.Command('iwn.put_on_random_diaper_accessory', command_type=(sims4.commands.CommandType.Live))
def put_on_random_diaper_accessory(owner_id:int=None, _connection=None, outfit_category_and_index=None, update_client=True):
    if not _ember_detected:
        return
    try:
        if owner_id is not None:
            sim_info = services.sim_info_manager().get(owner_id)
            if sim_info is not None:
                if sim_info.species != Species.HUMAN:
                    return
                logger.info("iwn.put_on_random_diaper_accessory: {}", sim_info)
                if outfit_category_and_index is None:
                    outfit_category_and_index = sim_info.get_current_outfit()
                if outfit_category_and_index is not None:
                    if outfit_category_and_index[0] in outfit_categories_excluded_from_diaper:
                        return
                    outfit_parts = get_outfit_parts(sim_info, outfit_category_and_index)
                    if outfit_parts is not None:

                        if BodyType.LOWER_BODY in outfit_parts.keys():
                            for outfit_part in outfit_parts[BodyType.LOWER_BODY]:
                                if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                                    return

                        if sim_info.age in (Age.TEEN, Age.YOUNGADULT, Age.ADULT, Age.ELDER):
                            if BodyType.INDEX_FINGER_LEFT in outfit_parts.keys():
                                for outfit_part in outfit_parts[BodyType.INDEX_FINGER_LEFT]:
                                    if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                                        return
                            else:
                                outfit_parts[BodyType.INDEX_FINGER_LEFT] = (CasPart((0)),)

                        elif _admin_flag and sim_info.age == Age.CHILD:
                            if BodyType.EARRINGS in outfit_parts.keys():
                                for outfit_part in outfit_parts[BodyType.EARRINGS]:
                                    if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                                        return
                            else:
                                outfit_parts[BodyType.EARRINGS] = (CasPart((0)),)

                        diaper_part_id = None

                        if has_trait(sim_info.id, NativeTrait.GENDER_OPTIONS_FRAME_MASCULINE):
                            diaper_part_id = random.choice(
                                DiaperLoadCASConfig.get_default_diaper_parts_ids_for_body_type(BodyType.INDEX_FINGER_LEFT,
                                                                                               _male_accessory))
                        elif has_trait(sim_info.id, NativeTrait.GENDER_OPTIONS_FRAME_FEMININE):
                            diaper_part_id = random.choice(
                                DiaperLoadCASConfig.get_default_diaper_parts_ids_for_body_type(BodyType.INDEX_FINGER_LEFT,
                                                                                               _female_accessory))
                        if diaper_part_id is not None:
                            if sim_info.age in (Age.TEEN, Age.YOUNGADULT, Age.ADULT, Age.ELDER):
                                outfit_parts[BodyType.INDEX_FINGER_LEFT] = (CasPart((diaper_part_id)),)
                            elif _admin_flag and sim_info.age == Age.CHILD:
                                outfit_parts[BodyType.EARRINGS] = (CasPart((16089036029714611952)),)
                            set_outfit_parts(sim_info, outfit_category_and_index, outfit_parts, update_client)
    except Exception as e:
        logger.error("put_on_random_diaper_accessory failed to run.")
        logger.error(traceback.format_exc())


@sims4.commands.Command('iwn.remove_diaper', command_type=(sims4.commands.CommandType.Live))
def remove_diaper(owner_id:int=None, _connection=None, force_remove=False, outfit_category_and_index=None, update_client=True):
    # if not _ember_detected:
    #     return
    try:
        if owner_id is not None:
            for buff in remove_diaper_buffs:
                if has_buff(owner_id, buff):
                    force_remove = True
            if not force_remove:
                if is_wearing_diaper(owner_id):
                    return
                # if always_wears_diapers(owner_id):
                #     return
                # for buff in force_diaper_pants_buffs:
                #     if has_buff(owner_id, buff):
                #         return
                # for buff in force_diaper_accessory_buffs:
                #     if has_buff(owner_id, buff):
                #         return
            sim_info = services.sim_info_manager().get(owner_id)
            if sim_info is not None:
                if sim_info.species != Species.HUMAN:
                    return
                logger.info("remove_diaper: {}", sim_info)
                if outfit_category_and_index is None:
                    outfit_category_and_index = sim_info.get_current_outfit()
                if outfit_category_and_index is not None:
                    if not force_remove:
                        if outfit_category_and_index[0] in outfit_categories_excluded_from_diaper:
                            return
                    # logger.info('current_outfit: {}'.format(current_outfit))
                    outfit_parts = get_outfit_parts(sim_info, outfit_category_and_index)
                    if outfit_parts is not None:
                        if BodyType.LOWER_BODY in outfit_parts.keys():
                            for outfit_part in outfit_parts[BodyType.LOWER_BODY]:
                                if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                                    logger.info("remove_diaper on LOWER_BODY: {}", sim_info)
                                    outfit_parts.pop(BodyType.LOWER_BODY, None)
                                    set_outfit_parts(sim_info, outfit_category_and_index, outfit_parts, update_client)
                        if BodyType.INDEX_FINGER_LEFT in outfit_parts.keys():
                            for outfit_part in outfit_parts[BodyType.INDEX_FINGER_LEFT]:
                                if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                                    logger.info("remove_diaper on INDEX_FINGER_LEFT: {}", sim_info)
                                    outfit_parts.pop(BodyType.INDEX_FINGER_LEFT, None)
                                    set_outfit_parts(sim_info, outfit_category_and_index, outfit_parts, update_client)
                        if _admin_flag and sim_info.age == Age.CHILD and BodyType.EARRINGS in outfit_parts.keys():
                            for outfit_part in outfit_parts[BodyType.EARRINGS]:
                                if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                                    logger.info("remove_diaper on EARRINGS: {}", sim_info)
                                    outfit_parts.pop(BodyType.EARRINGS, None)
                                    set_outfit_parts(sim_info, outfit_category_and_index, outfit_parts, update_client)
    except Exception as e:
        logger.error("remove_diaper failed to run.")
        logger.error(traceback.format_exc())


def get_modified_diaper_outfit_parts(original_parts, wetness_level, mess_level):
    outfit_parts = original_parts

    if outfit_parts is None:
        return EMPTY_DICT

    needs_outfit_change = False

    for body_type, outfit_part_tuple in original_parts.items():
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


def have_pants_changed(sim_info, current_outfit, previous_outfit):
    if current_outfit is not None and previous_outfit is not None:
        if previous_outfit[0] == current_outfit[0] and previous_outfit[1] == current_outfit[1]:
            return False
        current_parts = get_outfit_parts(sim_info, current_outfit)
        previous_parts = get_outfit_parts(sim_info, previous_outfit)

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


def get_diaper_parts(outfit_parts, include_bottom:bool=True, include_accessory:bool=True):
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


def is_diaper_removed(sim_info, current_outfit, previous_outfit):
    return is_diaper_accessory_removed(sim_info, current_outfit, previous_outfit) or is_diaper_bottom_removed(sim_info, current_outfit, previous_outfit)


def is_diaper_accessory_removed(sim_info, current_outfit, previous_outfit):
    if current_outfit is not None and previous_outfit is not None:
        # if previous_outfit[0] == current_outfit[0] and previous_outfit[1] == current_outfit[1]:
        #     return False
        current_parts = get_outfit_parts(sim_info, current_outfit)
        previous_parts = get_outfit_parts(sim_info, previous_outfit)

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
            if _admin_flag and sim_info.age == Age.CHILD and BodyType.EARRINGS in previous_parts.keys():
                for outfit_part in previous_parts[BodyType.EARRINGS]:
                    if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                        had_diaper = True
                        break
                if had_diaper:
                    if BodyType.EARRINGS not in current_parts.keys():
                        return True
                    for outfit_part in current_parts[BodyType.EARRINGS]:
                        if DiaperLoadCASConfig.is_diaper_part(outfit_part.cas_part):
                            return False
                    return True

    return False


def is_diaper_bottom_removed(sim_info, current_outfit, previous_outfit):
    if current_outfit is not None and previous_outfit is not None:
        # if previous_outfit[0] == current_outfit[0] and previous_outfit[1] == current_outfit[1]:
        #     return False
        current_parts = get_outfit_parts(sim_info, current_outfit)
        previous_parts = get_outfit_parts(sim_info, previous_outfit)

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


def apply_outfit_parts_for_diaper_load(sim_info=None,outfit_category_and_index=None,update_client=True):
    try:
        if sim_info is not None:
            logger.info("apply_outfit_parts_for_diaper_load: {}", sim_info)
            wetness_level = get_statistic_value(sim_info, IwnBedwettingStatistic.DIAPER_WETNESS) or 0
            mess_level = get_statistic_value(sim_info, IwnBedwettingStatistic.DIAPER_MESSINESS) or 0
            logger.info("diaper wetness: {}", wetness_level)
            logger.info("diaper messiness: {}", mess_level)

            if outfit_category_and_index is None:
                outfit_category_and_index = sim_info.get_current_outfit()

            original_parts = get_outfit_parts(sim_info, outfit_category_and_index)

            logger.info("original_parts {}", original_parts)



            modified_parts = get_modified_diaper_outfit_parts(original_parts, wetness_level, mess_level)

            if modified_parts is not None:
                set_outfit_parts(sim_info, outfit_category_and_index, modified_parts, update_client)
    except Exception as e:
        logger.error("apply_outfit_parts_for_diaper_load encountered an error.")
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


def get_statistic_value(sim_info, statistic_id):
    value = None
    if sim_info is not None and statistic_id is not None:
        statistic_instance = _get_statistic_manager().get(statistic_id)
        if statistic_instance is not None:
            if sim_info.has_component(objects.components.types.STATISTIC_COMPONENT):
                statistics_component = sim_info.get_component(objects.components.types.STATISTIC_COMPONENT)
                if statistics_component is not None:
                    statistics_tracker = statistics_component.get_tracker(statistic_instance)
                    if statistics_tracker is not None:
                        statistic = statistics_tracker.get_statistic(statistic_instance)
                        if statistic is not None:
                            return statistic.get_value()
    return value


NO_COLOR_SHIFT = 4611686018427387904


class CasPart:

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
        return "CasPart({}, color_shift={}, object_id={}, layer_id={})".format(self.cas_part, self.color_shift, self.object_id, self.layer_id)


def set_outfit_parts(sim_info, outfit_category_and_index, outfit_parts, update_client=True):
    outfit_data = sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])
    if outfit_data is None:
        return
    logger.info('outfit_data: {}'.format(outfit_data))
    outfit_body_types = []
    outfit_part_ids = []
    outfit_color_shifts = []
    outfit_object_ids = []
    outfit_layer_ids = []
    for (body_type, cas_part_or_seq) in outfit_parts.items():
        if body_type == -1:
            continue
        if isinstance(cas_part_or_seq, tuple):
            if not cas_part_or_seq:
                continue
        elif cas_part_or_seq.cas_part == -1:
            continue
        else:
            cas_part_or_seq = (
             cas_part_or_seq,)
        for cas_part in cas_part_or_seq:
            if cas_part.cas_part == -1:
                continue
            outfit_body_types.append(body_type)
            outfit_part_ids.append(cas_part.cas_part)
            outfit_color_shifts.append(cas_part.color_shift)
            outfit_object_ids.append(cas_part.object_id)
            outfit_layer_ids.append(cas_part.layer_id)

        apply(sim_info, outfit_body_types, outfit_part_ids, outfit_color_shifts, outfit_object_ids, outfit_layer_ids, outfit_category_and_index, update_client)


def apply(sim_info, outfit_body_types=[], outfit_part_ids=[], outfit_color_shifts=[], outfit_object_ids=[], outfit_layer_ids=[], outfit_category_and_index=None, update_client=True,):
    outfits_msg = sim_info.save_outfits()
    if outfit_category_and_index is None:
        outfit_category_and_index = sim_info.get_current_outfit()
    outfit_id = getattr(sim_info.get_outfit(outfit_category_and_index[0],outfit_category_and_index[1]), 'outfit_id', 0)

    for outfit in outfits_msg.outfits:
        if outfit.category != int(outfit_category_and_index[0]):
            # logger.info("wrong outfit category. expected {} got {}",current_outfit[0], outfit.category)
            continue
        if outfit.outfit_id != outfit_id:
            # logger.info("wrong outfit id. expected {} got {}",outfit_id, outfit.outfit_id)
            continue
        else:
            outfit.parts = S4Common_pb2.IdList()
            outfit.parts.ids.extend(outfit_part_ids)
            outfit.body_types_list = Outfits_pb2.BodyTypesList()
            outfit.body_types_list.body_types.extend(outfit_body_types)
            outfit.part_shifts = Outfits_pb2.ColorShiftList()
            outfit.part_shifts.color_shift.extend(outfit_color_shifts)
            outfit.object_ids = Outfits_pb2.ObjectIdsList()
            outfit.object_ids.object_id.extend(outfit_object_ids)
            outfit.layer_ids = Outfits_pb2.LayerIdsList()
            outfit.layer_ids.layer_id.extend(outfit_layer_ids)
            break
    sim_info._base.outfits = outfits_msg.SerializeToString()
    # logger.info('outfit {}', sim_info._base.outfits)
    # sim_info._base.outfit_type_and_index = current_outfit
    # sim_info.set_outfit_dirty(outfit_category_and_index[0])
    if update_client:
        sim_info.resend_outfits()
        # sim_info.appearance_tracker.evaluate_appearance_modifiers()


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


@sims4.commands.Command('iwn.open_loverslab_club', command_type=(sims4.commands.CommandType.Live))
def open_loverslab_club(_connection=None):
    webbrowser.open("https://www.loverslab.com/clubs/9-little-space-private-abdl-mods-and-forums/")
    services.game_clock_service().set_clock_speed(ClockSpeedMode.PAUSED)

@sims4.commands.Command('iwn.open_mod_page', command_type=(sims4.commands.CommandType.Live))
def open_mod_page(_connection=None):
    webbrowser.open("https://www.loverslab.com/files/file/28368-iwnbedwetting-extended/")
    services.game_clock_service().set_clock_speed(ClockSpeedMode.PAUSED)

@sims4.commands.Command('iwn.open_ember_mod_page', command_type=(sims4.commands.CommandType.Live))
def open_ember_mod_page(_connection=None):
    webbrowser.open("https://www.loverslab.com/files/file/30769-universal-adult-diaper-with-automatic-bulge-and-peek-effects-female-and-male/")
    services.game_clock_service().set_clock_speed(ClockSpeedMode.PAUSED)


@sims4.commands.Command('iwn.set_statistic_value', command_type=(sims4.commands.CommandType.Live))
def set_statistic_value(owner_id:int=None, statistic_id=None, new_value=None, _connection=None):
    if owner_id is not None and statistic_id is not None and new_value is not None:
        # output = sims4.commands.CheatOutput(_connection)
        sim_info = services.sim_info_manager().get(owner_id)
        if sim_info is not None:
            # output('Setting statistic {} on {} to {}'.format(statistic_id, sim_info, new_value))
            statistic_instance = _get_statistic_manager().get(int(statistic_id))
            if statistic_instance is not None:
                if not sim_info.has_component(objects.components.types.STATISTIC_COMPONENT):
                    if isinstance(sim_info, ComponentContainer):
                        if hasattr(sim_info, 'add_dynamic_component'):
                            sim_info.add_dynamic_component(objects.components.types.STATISTIC_COMPONENT)
                statistics_component = sim_info.get_component(objects.components.types.STATISTIC_COMPONENT)
                if statistics_component is not None:
                    statistics_tracker = statistics_component.get_tracker(statistic_instance)
                    if statistics_tracker is not None:
                        statistics_tracker.set_value(statistic_instance, (_filter_value(new_value)), add=True)


@sims4.commands.Command('iwn.remove_statistic', command_type=(sims4.commands.CommandType.Live))
def remove_statistic(owner_id:int=None, statistic_id=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    sim_info = services.sim_info_manager().get(owner_id)
    if sim_info is not None:
        output('Removing statistic {} on {}'.format(statistic_id, sim_info))
        statistic_instance = _get_statistic_manager().get(int(statistic_id))
        if statistic_instance is not None:
            if sim_info.has_component(objects.components.types.STATISTIC_COMPONENT):
                statistics_component = sim_info.get_component(objects.components.types.STATISTIC_COMPONENT)
                if statistics_component is not None:
                    statistics_tracker = statistics_component.get_tracker(statistic_instance)
                    if statistics_tracker is not None:
                        statistics_tracker.remove_statistic(statistic_instance)


def remove_statistics(sim_info, statistics):
    if sim_info is not None:
        if sim_info.has_component(objects.components.types.STATISTIC_COMPONENT):
            statistics_component = sim_info.get_component(objects.components.types.STATISTIC_COMPONENT)
            if statistics_component is not None:
                for statistic_id in statistics:
                    statistic_instance = _get_statistic_manager().get(int(statistic_id))
                    if statistic_instance is not None:
                        statistics_tracker = statistics_component.get_tracker(statistic_instance)
                        if statistics_tracker is not None:
                            statistics_tracker.remove_statistic(statistic_instance)


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


sleeping_diaper_usage_affordances = (15386335300547775969, 17846418620694466401, 14347203327565699161, 15545876685594118345)
motive_bladder = 16652
bladder_control_test_guid = 15794548069054423667

forced_compatibility_affordances = ()




@inject(InstanceManager, 'load_data_into_class_instances')
def modify_sleep_affordances(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        if self.TYPE != Types.INTERACTION:
            return result

        logger.info('Injecting Sleep Affordances')
        bladder_control_test = services.snippet_manager().get(bladder_control_test_guid)

        affordance_manager = services.affordance_manager()
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
                                        if condition._tuned_values.stat.guid64 == motive_bladder:
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
toilet_global_test_id = 15481261038742746897
loot_diaper_dependence_used_potty_id = 14520123767131912383


@inject(InstanceManager, 'load_data_into_class_instances')
def block_toilet_for_diapered_sims(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        if self.TYPE != Types.INTERACTION:
            return result

        logger.info('Injecting Toilet Affordances')

        snippet_manager = services.snippet_manager()
        toilet_autonomy_test = snippet_manager.get(toilet_autonomy_test_id)
        toilet_global_test = snippet_manager.get(toilet_global_test_id)

        affordance_manager = services.affordance_manager()
        for guid in InteractionSets.TOILET_USE_INTERACTIONS:
            tun = affordance_manager.get(guid)
            if tun is not None:
                logger.info('{}'.format(tun))
                if hasattr(tun, 'test_autonomous') and len(tun.test_autonomous) > 0:
                    # logger.info('{}'.format(tun.test_autonomous))
                    # logger.info('{}'.format(tun.test_autonomous.__class__))
                    for idx, test_group in enumerate(tun.test_autonomous):
                        # logger.info('{}'.format(tun.test_autonomous[idx].__class__))
                        # logger.info('{}'.format(tun.test_autonomous[idx]))
                        if toilet_autonomy_test not in test_group:
                            tun.test_autonomous[idx] = test_group + (toilet_autonomy_test,)
                            # logger.info('{}'.format(tun.test_autonomous[idx]))
                        # else:
                        #     logger.info('Toilet autonomy already fixed')
                        #     logger.info('{}'.format(tun.test_autonomous[idx]))
                else:
                    tun.test_autonomous = CompoundTestList()
                    tun.test_autonomous.append((toilet_autonomy_test,))
                    # tun.test_autonomous[0] = (toilet_autonomy_test,)
                    # tun.test_autonomous.append(list((toilet_autonomy_test,)))
                    # logger.info('{}'.format(tun.test_autonomous))
                #
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
                tuned_values['loot_list'] = tuple(loot_list)
                immutable_slots_cls = sims4.collections.make_immutable_slots_class(tuned_values.keys())
                tuned_values = immutable_slots_cls(tuned_values)
                e = TunableFactory.TunableFactoryWrapper(tuned_values, LootElement.__name__, LootElement)
                tun.basic_extras = tun.basic_extras + (e,)
                # logger.info('{}'.format(tun.basic_extras))


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




@inject(InstanceManager, 'load_data_into_class_instances')
def little_autonomy_fixer(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        if self.TYPE != Types.INTERACTION:
            return result

        logger.info('Injecting Little Autonomy Fixes')

        little_autonomy_targets = [30917]

        little_autonomy_tests = [15768591105414661584]

        excluded_interactions = [16617239709778473043, 10785441443215295256,287675,276860,287683,287681,280987,275341,319632,274023,274891,326839,156159,277492,277490,277498,277497,308458,308459,151786,151827,153920,146042,146041,155696,144287]

        posture_buffs = [144745,280280,280281,280282]

        snippet_manager = services.snippet_manager()
        little_autonomy_test_instances = [snippet_manager.get(x) for x in little_autonomy_tests]

        standard_test = snippet_manager.get(15768591105414661584)
        social_test = snippet_manager.get(13514748390442777472)

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

    mods = get_mods_files_info()

    if _old_mods_detected:
        # localized_title = lambda **_: LocalizationHelperTuning.get_raw_text('WARNING: IwnBedWetting Extended+ Old Files Detected')
        # localized_text = lambda **_: LocalizationHelperTuning.get_raw_text('Please delete ALL LilNinthel packages EXCEPT for LilNinthel_IWNBedwetting_Extended_Plus.package or the mod may not function correctly')
        # ShowNotificationInternal(localized_title, localized_text, None)
        dialog = UiDialogOk.TunableFactory().default(None)
        dialog.title = lambda **_: LocalizationHelperTuning.get_raw_text('WARNING: IWNBedWetting Extended+ Old Files Detected')
        dialog.text = lambda **_: LocalizationHelperTuning.get_raw_text('Please delete ALL LilNinthel .package files EXCEPT for LilNinthel_IWNBedwetting_Extended_Plus.package or the mod may not function correctly')
        dialog.show_dialog()

    if _old_addons_detected and not _admin_flag:
        # localized_title = lambda **_: LocalizationHelperTuning.get_raw_text('WARNING: IwnBedWetting Extended+ Old Files Detected')
        # localized_text = lambda **_: LocalizationHelperTuning.get_raw_text('Please delete ALL LilNinthel packages EXCEPT for LilNinthel_IWNBedwetting_Extended_Plus.package or the mod may not function correctly')
        # ShowNotificationInternal(localized_title, localized_text, None)
        dialog = UiDialogOk.TunableFactory().default(None)
        dialog.title = lambda **_: LocalizationHelperTuning.get_raw_text('WARNING: IWNBedWetting Extended+ Old Add-Ons Detected')
        dialog.text = lambda **_: LocalizationHelperTuning.get_raw_text('Please delete ALL previous versions of the following add-ons: Happily Diapered Extended by BabyLola, Unhappily Diapered Extended by Lil Luna, ABDL Extended by mackico, or Happily Messy Extended by DiaperDump. They are all now included with this mod and may cause issues.')
        dialog.show_dialog()

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





    xml_injector_spec = importlib.util.find_spec("xml_injector")
    found = xml_injector_spec is not None

    if not found:
        dialog = UiDialogOk.TunableFactory().default(None)
        dialog.title = lambda **_: LocalizationHelperTuning.get_raw_text('WARNING: IwnBedWetting Extended+ - XML Injector Not Detected')
        dialog.text = lambda **_: LocalizationHelperTuning.get_raw_text('This mod requires XML Injector to function. Please install the latest XML Injector from https://scumbumbomods.com/#/xml-injector/')
        dialog.show_dialog()

    logger.info("WickedWhims installed: {}".format(_wicked_whims_installed))

    ModHasRun = True
    # if devMode:
    #     modify_sleep_affordances()


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
