import services
from date_and_time import TimeSpan
from omutsulib.services.components_service import get_components_service, OmutsuComponentType
from omutsulib.wrappers.enum import OmutsuIntEnum
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class OmutsuObjectPreferenceTag(OmutsuIntEnum):
    LOVESEAT = 0
    BED = 1
    STUFFED_ANIMAL = 2
    INSTRUMENT = 3
    COMPUTER = 4
    FOOD = 5
    DRINK = 6
    TENT = 7
    FOOD_BOWL = 8
    PET_SLEEP_OBJECT = 9
    HORSE_BED = 10
    DANCING_POLE = 500
    DANCING_SPOT = 501
    DANCING_SIM = 502


class OmutsuAutonomyState(OmutsuIntEnum):
    UNDEFINED = -1
    DISABLED = 0
    LIMITED_ONLY = 1
    MEDIUM = 2
    FULL = 3


class OmutsuOffLotAutonomyRule(OmutsuIntEnum):
    DEFAULT = 0
    ON_LOT_ONLY = 1
    SHARED_SPACE_ONLY = 2
    OFF_LOT_ONLY = 3
    UNLIMITED = 4
    RESTRICTED = 5
    ANCHORED = 6
    BUSINESS_EMPLOYEE = 7
    BUSINESS_CUSTOMER = 8


class _OmutsuSimAutonomyMixin(_SuperOmutsuSim):

    def ping_autonomy(self, ticks=1):
        sim = self.get_sim_instance()
        if sim is not None:
            autonomy_component = get_components_service().get_object_component(sim, OmutsuComponentType.AUTONOMY)
            if autonomy_component is not None:
                autonomy_component._last_user_directed_action_time = None
                autonomy_component._schedule_next_full_autonomy_update(TimeSpan(ticks))

    def get_autonomy_state_setting(self):
        sim = self.get_sim_instance()
        if sim is not None:
            autonomy_component = get_components_service().get_object_component(sim, OmutsuComponentType.AUTONOMY)
            if autonomy_component is not None:
                return autonomy_component.get_autonomy_state_setting()
            return OmutsuAutonomyState.UNDEFINED

    def get_off_lot_autonomy_rule(self):
        sim = self.get_sim_instance()
        if sim is not None:
            sim_info = self.get_sim_info()
            if sim_info.is_npc:
                statistics_component = get_components_service().get_object_component(sim_info, OmutsuComponentType.STATISTIC)
                if statistics_component is not None:
                    return statistics_component.get_off_lot_autonomy_rule().rule
            return OmutsuOffLotAutonomyRule.DEFAULT

    def is_allowed_on_current_lot(self):
        sim = self.get_sim_instance()
        if sim is not None:
            autonomy_component = get_components_service().get_object_component(sim, OmutsuComponentType.AUTONOMY)
            if autonomy_component is not None:
                for role_state_instance in autonomy_component.active_roles():
                    if sim.is_npc:
                        if not role_state_instance._portal_disallowance_tags:
                            if not role_state_instance._allow_npc_routing_on_active_lot:
                                return False
                            else:
                                if role_state_instance._portal_disallowance_tags:
                                    return False

                return True
            return False

    def is_allowed_on_dynamic_area(self, dynamic_area_type):
        autonomy_rule = self.get_off_lot_autonomy_rule()
        for autonomy_restriction in services.dynamic_area_service().DYNAMIC_AREA_AUTONOMY_RESTRICTION:
            if autonomy_restriction.autonomy_rule == autonomy_rule:
                if dynamic_area_type in autonomy_restriction.area_types:
                    return False

        return True

    @sim_info_required(default=None)
    def get_object_scoring_preferred(self, object_preference_tag):
        sim_info = self.get_sim_info()
        return sim_info.autonomy_scoring_preferences.get(object_preference_tag, None)

    @sim_info_required()
    def set_object_scoring_preference(self, object_preference_tag, game_object):
        sim_info = self.get_sim_info()
        if game_object is not None:
            sim_info.autonomy_scoring_preferences[object_preference_tag] = game_object.id
        elif object_preference_tag in sim_info.autonomy_scoring_preferences:
            del sim_info.autonomy_scoring_preferences[object_preference_tag]

    @sim_info_required(default=False)
    def is_object_scoring_preferred(self, object_preference_tag, game_object):
        sim_info = self.get_sim_info()
        return sim_info.autonomy_scoring_preferences.get(object_preference_tag, None) == game_object.id

    @sim_info_required(default=None)
    def get_object_use_preferred(self, object_preference_tag):
        sim_info = self.get_sim_info()
        return sim_info.autonomy_use_preferences.get(object_preference_tag, None)

    @sim_info_required()
    def set_object_use_preference(self, object_preference_tag, game_object):
        sim_info = self.get_sim_info()
        if game_object is not None:
            sim_info.autonomy_use_preferences[object_preference_tag] = game_object.id
        elif object_preference_tag in sim_info.autonomy_use_preferences:
            del sim_info.autonomy_use_preferences[object_preference_tag]

    @sim_info_required(default=False)
    def is_object_use_preferred(self, object_preference_tag, game_object):
        sim_info = self.get_sim_info()
        if sim_info.autonomy_use_preferences.get(object_preference_tag, None) == game_object.id:
            return True
        object_preference_tracker = services.object_preference_tracker()
        if object_preference_tracker is not None:
            (object_id, _) = object_preference_tracker.get_restricted_object(sim_info.sim_id, object_preference_tag)
            if object_id == game_object.id:
                return True
            return False

    @sim_info_required()
    def has_autonomy_modifier(self, modifier_handle):
        sim_info = self.get_sim_info()
        statistics_component = get_components_service().get_object_component(sim_info, (OmutsuComponentType.STATISTIC), add_dynamic=True)
        if statistics_component is not None:
            return modifier_handle in statistics_component._statistic_modifiers
        return False

    @sim_info_required()
    def add_autonomy_modifier(self, modifier, modifier_handle=None, is_interaction_modifier=False):
        sim_info = self.get_sim_info()
        statistics_component = get_components_service().get_object_component(sim_info, (OmutsuComponentType.STATISTIC), add_dynamic=True)
        if statistics_component is not None:
            return statistics_component.add_statistic_modifier(modifier, requested_handle=modifier_handle, interaction_modifier=is_interaction_modifier)

    @sim_info_required()
    def remove_autonomy_modifier(self, modifier_handle):
        sim_info = self.get_sim_info()
        statistics_component = get_components_service().get_object_component(sim_info, (OmutsuComponentType.STATISTIC), add_dynamic=True)
        if statistics_component is not None:
            statistics_component.remove_statistic_modifier(modifier_handle)
