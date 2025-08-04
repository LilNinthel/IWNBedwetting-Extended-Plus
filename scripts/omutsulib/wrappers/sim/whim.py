import services
from situations.dynamic_situation_goal_tracker import DynamicSituationGoalTracker, ActivitySituationGoalTracker
from situations.situation_goal_tracker import SituationGoalTracker
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim

class _OmutsuSimWhimMixin(_SuperOmutsuSim):

    def complete_situation_goal(self, *situation_goal_ids, sim_identifier=None):
        sim = self.get_sim_instance()
        if sim is None:
            return
        from omutsulib.wrappers.sim.sim import OmutsuSim
        target_omutsu_sim = OmutsuSim(sim_identifier) if sim_identifier is not None else None
        goal_instances = []
        for situation in services.get_zone_situation_manager().get_situations_sim_is_in(sim):
            goal_tracker = situation._get_goal_tracker()
            if goal_tracker is not None:
                if isinstance(goal_tracker, SituationGoalTracker):
                    if goal_tracker._realized_minor_goals is not None:
                        goal_instances.extend(goal_tracker._realized_minor_goals.keys())
                    if goal_tracker._realized_main_goal is not None:
                        goal_instances.insert(0, goal_tracker._realized_main_goal)
                elif isinstance(goal_tracker, DynamicSituationGoalTracker):
                    goal_instances.extend(goal_tracker.goals)
                else:
                    if isinstance(goal_tracker, ActivitySituationGoalTracker):
                        if goal_tracker._main_goal is not None:
                            goal_instances.append(goal_tracker._main_goal)
                        goal_instances.extend(goal_tracker.goals)

        whims_tracker = self.get_sim_info().whim_tracker
        if whims_tracker is not None:
            for whim_slot in whims_tracker.slots_gen():
                if not whim_slot.is_empty():
                    goal_instances.append(whim_slot.goal_instance)

        for goal_instance in goal_instances:
            if goal_instance.guid64 in situation_goal_ids:
                if not goal_instance._valid_event_sim_of_interest(self.get_sim_info()):
                    continue
                elif target_omutsu_sim is not None:
                    goal_instance._actual_target_sim_info_id = target_omutsu_sim.get_sim_id()
                if goal_instance.completed_iterations < goal_instance.max_iterations:
                    goal_instance._increment_completion_count()
