import services
from statistics.skill import Skill, SkillLevelType
from omutsulib.services.components_service import get_components_service, OmutsuComponentType
from omutsulib.services.resources_service import get_resource_service, OmutsuResourceType
from omutsulib.services.service import OmutsuService
from omutsulib.wrappers.enum import OmutsuIntEnum
from omutsulib.wrappers.sim.sim import OmutsuSim

class OmutsuStatisticLockAction(OmutsuIntEnum):
    DO_NOT_CHANGE_VALUE = 0
    USE_MIN_VALUE_TUNING = 1
    USE_MAX_VALUE_TUNING = 2
    USE_BEST_VALUE_TUNING = 3


class OmutsuStatisticsService(OmutsuService):

    def has_statistic(self, instance, statistic_id):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        statistics_tracker = statistics_component.get_tracker(statistic_instance)
                        if statistics_tracker is not None:
                            if statistics_tracker._statistics:
                                if statistic_instance in statistics_tracker._statistics:
                                    stat = statistics_tracker._statistics[statistic_instance]
                                    if stat is not None:
                                        return True
        return False

    def remove_statistic(self, instance, statistic_id):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, OmutsuComponentType.STATISTIC)
                    if statistics_component is not None:
                        statistics_tracker = statistics_component.get_tracker(statistic_instance)
                        if statistics_tracker is not None:
                            statistics_tracker.remove_statistic(statistic_instance)

    def clear_statistic(self, instance, statistic_id):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, OmutsuComponentType.STATISTIC)
                    if statistics_component is not None:
                        statistics_tracker = statistics_component.get_tracker(statistic_instance)
                        if statistics_tracker is not None:
                            statistics_tracker.clear_statistic(statistic_instance)

    def set_statistic_value(self, instance, statistic_id, value, add=True):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        statistics_tracker = statistics_component.get_tracker(statistic_instance)
                        if statistics_tracker is not None:
                            statistics_tracker.set_value(statistic_instance, (_filter_value(value)), add=add)

    def change_statistic_value(self, instance, statistic_id, value, add=True):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        statistics_tracker = statistics_component.get_tracker(statistic_instance)
                        if statistics_tracker is not None:
                            statistics_tracker.add_value(statistic_instance, (_filter_value(value)), add=add)

    def get_statistic_value(self, instance, statistic_id, add=False, default=0):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        statistics_tracker = statistics_component.get_tracker(statistic_instance)
                        if statistics_tracker is not None:
                            statistic = statistics_tracker.get_statistic(statistic_instance, add=add)
                            if statistic is not None:
                                value = statistic.get_value() / 1
                                if value.is_integer():
                                    return int(value)
                                return value
                            if hasattr(statistic_instance, "get_initial_value"):
                                initial_value = statistic_instance.get_initial_value() / 1
                            else:
                                initial_value = statistic_instance.default_value / 1
                            if initial_value.is_integer():
                                return int(initial_value)
                        return initial_value
            return default

    def add_statistic_modifier(self, instance, statistic_id, modifier_value, add=False):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        statistics_tracker = statistics_component.get_tracker(statistic_instance)
                        if statistics_tracker is not None:
                            statistic = statistics_tracker.get_statistic(statistic_instance, add=add)
                            if statistic is not None:
                                statistic.add_statistic_modifier(modifier_value)

    def remove_statistic_modifier(self, instance, statistic_id, modifier_value, add=False):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        statistics_tracker = statistics_component.get_tracker(statistic_instance)
                        if statistics_tracker is not None:
                            statistic = statistics_tracker.get_statistic(statistic_instance, add=add)
                            if statistic is not None:
                                statistic.remove_statistic_modifier(modifier_value)

    def clear_statistic_modifiers(self, instance, statistic_id, add=False):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        statistics_tracker = statistics_component.get_tracker(statistic_instance)
                        if statistics_tracker is not None:
                            statistic = statistics_tracker.get_statistic(statistic_instance, add=add)
                            if statistic is not None:
                                if statistic._statistic_modifiers is not None:
                                    for modifier_value in list(statistic._statistic_modifiers):
                                        statistic.remove_statistic_modifier(modifier_value)

    def get_statistic_decay_rate(self, instance, statistic_id, use_decay_modifier=True):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        statistics_tracker = statistics_component.get_tracker(statistic_instance)
                        if statistics_tracker is not None:
                            statistic = statistics_tracker.get_statistic(statistic_instance, add=False)
                            if statistic is not None:
                                return statistic.get_decay_rate(use_decay_modifier=use_decay_modifier)
            return 0.0

    def get_statistic_decay_rate_modifier(self, instance, statistic_id):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        statistics_tracker = statistics_component.get_tracker(statistic_instance)
                        if statistics_tracker is not None:
                            statistic = statistics_tracker.get_statistic(statistic_instance, add=False)
                            if statistic is not None:
                                return statistic.get_decay_rate_modifier()
            return 1.0

    def is_statistic_locked(self, instance, statistic_id):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        return statistics_component.is_stat_type_locked(statistic_instance)
            return False

    def get_statistic_locked_count(self, instance, statistic_id):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        if statistic_instance in statistics_component._locked_commodities:
                            return statistics_component._locked_commodities[statistic_instance]
            return 0

    def lock_statistic(self, instance, statistic_id, lock_action=OmutsuStatisticLockAction.DO_NOT_CHANGE_VALUE, lock_reason="iwnbedwetting"):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        return statistics_component.lock_statistic(statistic_instance, lock_action, "locked by {} at {}".format(lock_reason, services.time_service().sim_now))
            return False

    def unlock_statistic(self, instance, statistic_id, unlock_reason='iwnbedwetting', auto_satisfy=True):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        if statistic_instance in statistics_component._locked_commodities:
                            statistics_component.unlock_statistic(statistic_instance, ("unlocked by {} at {}".format(unlock_reason, services.time_service().sim_now)), auto_satisfy=auto_satisfy)
                            return True
            return False

    def add_statistic_watcher(self, instance, callback):
        if hasattr(instance, "is_sim") and instance.is_sim:
            omutsu_sim = OmutsuSim(instance)
            if omutsu_sim is not None:
                instance = omutsu_sim.get_sim_info()
            if instance is not None:
                statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                if statistics_component is not None:
                    commodity_tracker = statistics_component.get_commodity_tracker()
                    return commodity_tracker.add_watcher(callback)

    def remove_statistic_watcher(self, instance, handle_id):
        if hasattr(instance, "is_sim") and instance.is_sim:
            omutsu_sim = OmutsuSim(instance)
            if omutsu_sim is not None:
                instance = omutsu_sim.get_sim_info()
            if instance is not None:
                statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                if statistics_component is not None:
                    commodity_tracker = statistics_component.get_commodity_tracker()
                    if commodity_tracker.has_watcher_watcher(handle_id):
                        commodity_tracker.remove_watcher(handle_id)

    def get_initial_statistic_value(self, statistic_id):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            if hasattr(statistic_instance, "get_initial_value"):
                initial_value = statistic_instance.get_initial_value() / 1
            else:
                initial_value = statistic_instance.default_value / 1
            if initial_value.is_integer():
                return int(initial_value)
            return initial_value
        return 0

    def get_min_statistic_value(self, statistic_id):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            min_value = statistic_instance.min_value / 1
            if min_value.is_integer():
                return int(min_value)
            return min_value
        return 0

    def get_max_statistic_value(self, statistic_id):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, statistic_id)
        if statistic_instance is not None:
            max_value = statistic_instance.max_value / 1
            if max_value.is_integer():
                return int(max_value)
            return max_value
        return 1


class OmutsuSkillsService(OmutsuService):

    def has_skill(self, sim_identifier, skill_id):
        return get_statistics_service().has_statistic(sim_identifier, skill_id)

    def remove_skill(self, sim_identifier, skill_id):
        get_statistics_service().remove_statistic(sim_identifier, skill_id)

    def set_skill_value(self, sim_identifier, skill_id, value, add=True):
        get_statistics_service().set_statistic_value(sim_identifier, skill_id, value, add=add)

    def set_skill_level(self, sim_identifier, skill_id, level, add=True):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, skill_id)
        if statistic_instance is not None:
            omutsu_sim = OmutsuSim(sim_identifier)
            if omutsu_sim is not None:
                statistics_component = get_components_service().get_object_component((omutsu_sim.get_sim_info()), (OmutsuComponentType.STATISTIC), add_dynamic=True)
                if statistics_component is not None:
                    skills_tracker = statistics_component.get_tracker(statistic_instance)
                    if skills_tracker is not None:
                        tracked_skill = skills_tracker.get_statistic(statistic_instance, add=add)
                        if tracked_skill is not None:
                            return tracked_skill.set_user_value(level)

    def set_skill_level_value(self, sim_identifier, skill_id, value, add=True):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, skill_id)
        if statistic_instance is not None:
            omutsu_sim = OmutsuSim(sim_identifier)
            if omutsu_sim is not None:
                statistics_component = get_components_service().get_object_component((omutsu_sim.get_sim_info()), (OmutsuComponentType.STATISTIC), add_dynamic=True)
                if statistics_component is not None:
                    skills_tracker = statistics_component.get_tracker(statistic_instance)
                    if skills_tracker is not None:
                        tracked_skill = skills_tracker.get_statistic(statistic_instance, add=add)
                        if tracked_skill is not None:
                            level = tracked_skill.get_user_value()
                            value_for_level = tracked_skill.get_skill_value_for_level(level)
                            value_for_next_level = tracked_skill.get_skill_value_for_level(min(tracked_skill.max_level, level + 1)) - value_for_level
                            self.set_skill_value(sim_identifier, skill_id, value_for_level + value_for_next_level * value)

    def change_skill_value(self, sim_identifier, skill_id, value, add=True):
        get_statistics_service().change_statistic_value(sim_identifier, skill_id, value, add=add)

    def change_skill_level_value(self, sim_identifier, skill_id, value, add=True):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, skill_id)
        if statistic_instance is not None:
            omutsu_sim = OmutsuSim(sim_identifier)
            if omutsu_sim is not None:
                statistics_component = get_components_service().get_object_component((omutsu_sim.get_sim_info()), (OmutsuComponentType.STATISTIC), add_dynamic=True)
                if statistics_component is not None:
                    skills_tracker = statistics_component.get_tracker(statistic_instance)
                    if skills_tracker is not None:
                        tracked_skill = skills_tracker.get_statistic(statistic_instance, add=add)
                        if tracked_skill is not None:
                            if not tracked_skill.reached_max_level:
                                level = tracked_skill.get_user_value()
                                value_for_level = tracked_skill.get_skill_value_for_level(level)
                                value_for_next_level = tracked_skill.get_skill_value_for_level(min(tracked_skill.max_level, level + 1)) - value_for_level
                                value = value_for_next_level / 100 * value
                                if tracked_skill.get_value() < tracked_skill.initial_value:
                                    value = max(tracked_skill.initial_value, value)
                                self.change_skill_value(sim_identifier, skill_id, value)

    def get_skill_value(self, sim_identifier, skill_id, add=False):
        return get_statistics_service().get_statistic_value(sim_identifier, skill_id, add=add)

    def get_skill_level(self, sim_identifier, skill_id, add=False):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, skill_id)
        if statistic_instance is not None:
            omutsu_sim = OmutsuSim(sim_identifier)
            if omutsu_sim is not None:
                statistics_component = get_components_service().get_object_component((omutsu_sim.get_sim_info()), (OmutsuComponentType.STATISTIC), add_dynamic=True)
                if statistics_component is not None:
                    skills_tracker = statistics_component.get_tracker(statistic_instance)
                    if skills_tracker is not None:
                        tracked_skill = skills_tracker.get_statistic(statistic_instance, add=add)
                        if tracked_skill is not None:
                            return tracked_skill.get_user_value()
            return 1

    def get_skill_level_value(self, sim_identifier, skill_id, add=False):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, skill_id)
        if statistic_instance is not None:
            omutsu_sim = OmutsuSim(sim_identifier)
            if omutsu_sim is not None:
                statistics_component = get_components_service().get_object_component((omutsu_sim.get_sim_info()), (OmutsuComponentType.STATISTIC), add_dynamic=True)
                if statistics_component is not None:
                    skills_tracker = statistics_component.get_tracker(statistic_instance)
                    if skills_tracker is not None:
                        tracked_skill = skills_tracker.get_statistic(statistic_instance, add=add)
                        if tracked_skill is not None:
                            level = tracked_skill.get_user_value()
                            value = tracked_skill.get_value()
                            value_for_level = tracked_skill.get_skill_value_for_level(level)
                            value_for_next_level = tracked_skill.get_skill_value_for_level(min(tracked_skill.max_level, level + 1)) - value_for_level
                            if value_for_level > 0.0:
                                if value_for_next_level > 0.0:
                                    return (value - value_for_level) / value_for_next_level
            return 0

    def get_skill_absolute_level(self, sim_identifier, skill_id, add=False):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, skill_id)
        if statistic_instance is not None:
            omutsu_sim = OmutsuSim(sim_identifier)
            if omutsu_sim is not None:
                statistics_component = get_components_service().get_object_component((omutsu_sim.get_sim_info()), (OmutsuComponentType.STATISTIC), add_dynamic=True)
                if statistics_component is not None:
                    skills_tracker = statistics_component.get_tracker(statistic_instance)
                    if skills_tracker is not None:
                        tracked_skill = skills_tracker.get_statistic(statistic_instance, add=add)
                        if tracked_skill is not None:
                            return tracked_skill.get_user_value() + self.get_skill_level_value(sim_identifier, skill_id, add=add)
            return 1.0 + self.get_skill_level_value(sim_identifier, skill_id, add=add)

    def has_reached_skill_max_level(self, sim_identifier, skill_id):
        statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, skill_id)
        if statistic_instance is not None:
            omutsu_sim = OmutsuSim(sim_identifier)
            if omutsu_sim is not None:
                statistics_component = get_components_service().get_object_component((omutsu_sim.get_sim_info()), (OmutsuComponentType.STATISTIC), add_dynamic=True)
                if statistics_component is not None:
                    skills_tracker = statistics_component.get_tracker(statistic_instance)
                    if skills_tracker is not None:
                        tracked_skill = skills_tracker.get_statistic(statistic_instance, add=False)
                        if tracked_skill is not None:
                            return tracked_skill.reached_max_level
            return False

    def get_max_skill_value(self, skill_id):
        skill_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, skill_id)
        if skill_instance is not None:
            return skill_instance.get_max_skill_value()
        return Skill.SKILL_LEVEL_LIST.get(SkillLevelType.MAJOR)

    def get_max_skill_level(self, skill_id):
        skill_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, skill_id)
        if skill_instance is not None:
            return skill_instance.max_level
        return 10


_STATISTICS_SERVICE = OmutsuStatisticsService("statistics")
_SKILLS_SERVICE = OmutsuSkillsService("skills")

def get_statistics_service() -> OmutsuStatisticsService:
    return _STATISTICS_SERVICE


def get_skills_service() -> OmutsuSkillsService:
    return _SKILLS_SERVICE


def _filter_value(value):
    try:
        return float(value)
    except ValueError:
        pass

    return int(value)
