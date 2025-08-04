from event_testing.event_data_const import ObjectiveDataStorageType
from omutsulib.services.resources_service import get_resource_service, OmutsuResourceType
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class _OmutsuSimAspirationsMixin(_SuperOmutsuSim):

    @sim_info_required(default=0)
    def get_active_aspiration(self):
        sim_info = self.get_sim_info()
        aspiration_tracker = sim_info.aspiration_tracker
        if aspiration_tracker is not None:
            return getattr(aspiration_tracker._active_aspiration, "guid64", 0)
        return 0

    @sim_info_required(default=0)
    def is_aspiration_tracker_objective_completed(self, objective_id):
        sim_info = self.get_sim_info()
        aspiration_tracker = sim_info.aspiration_tracker
        if aspiration_tracker is not None:
            objective_instance = get_resource_service().get_instance(OmutsuResourceType.OBJECTIVE, objective_id)
            if objective_instance is not None:
                return aspiration_tracker.objective_completed(objective_instance)
            return False

    @sim_info_required(default=0)
    def get_aspiration_tracker_objective_value(self, objective_id):
        sim_info = self.get_sim_info()
        aspiration_tracker = sim_info.aspiration_tracker
        if aspiration_tracker is not None:
            objective_instance = get_resource_service().get_instance(OmutsuResourceType.OBJECTIVE, objective_id)
            if objective_instance is not None:
                return aspiration_tracker.data_object.get_objective_count(objective_instance)
            return 0

    @sim_info_required()
    def change_aspiration_tracker_objective_value(self, aspiration_id, objective_id, value):
        sim_info = self.get_sim_info()
        aspiration_tracker = sim_info.aspiration_tracker
        if aspiration_tracker is not None:
            aspiration_instance = get_resource_service().get_instance(OmutsuResourceType.ASPIRATION, aspiration_id)
            objective_instance = get_resource_service().get_instance(OmutsuResourceType.OBJECTIVE, objective_id)
            if objective_instance is not None:
                if objective_instance.data_type == ObjectiveDataStorageType.CountData:
                    objective_count = aspiration_tracker.data_object.get_objective_count(objective_instance)
                    value = min(objective_count + value, objective_instance.goal_value())
                    completed_objectives = []
                    if value != objective_count:
                        aspiration_tracker.data_object.set_objective_value(objective_instance, value)
                        aspiration_tracker.update_objective(objective_instance, value, objective_instance.goal_value(), objective_instance.is_goal_value_money, objective_instance.show_progress, True)
                        if value >= objective_instance.goal_value():
                            if not aspiration_tracker.objective_completed(objective_instance):
                                aspiration_tracker.complete_objective(objective_instance, aspiration_instance)
                                completed_objectives.append(objective_instance)
                    self._try_complete_milestone(sim_info, aspiration_instance, objective_instances=completed_objectives)
                elif objective_instance.data_type == ObjectiveDataStorageType.IdData:
                    aspiration_tracker.data_object.add_objective_value(objective_instance, value)
                    objective_count = aspiration_tracker.data_object.get_objective_count(objective_instance)
                    aspiration_tracker.update_objective(objective_instance, objective_count, objective_instance.goal_value(), objective_instance.is_goal_value_money, objective_instance.show_progress, True)
                    completed_objectives = []
                    if objective_count >= objective_instance.goal_value():
                        if not aspiration_tracker.objective_completed(objective_instance):
                            aspiration_tracker.complete_objective(objective_instance, aspiration_instance)
                            completed_objectives.append(objective_instance)
                    self._try_complete_milestone(sim_info, aspiration_instance, objective_instances=completed_objectives)

    @sim_info_required()
    def set_aspiration_tracker_objective_value(self, aspiration_id, objective_id, value):
        sim_info = self.get_sim_info()
        aspiration_tracker = sim_info.aspiration_tracker
        if aspiration_tracker is not None:
            aspiration_instance = get_resource_service().get_instance(OmutsuResourceType.ASPIRATION, aspiration_id)
            objective_instance = get_resource_service().get_instance(OmutsuResourceType.OBJECTIVE, objective_id)
            if objective_instance is not None:
                if objective_instance.data_type == ObjectiveDataStorageType.CountData:
                    value = min(value, objective_instance.goal_value())
                    aspiration_tracker.data_object.set_objective_value(objective_instance, value)
                    aspiration_tracker.update_objective(objective_instance, value, objective_instance.goal_value(), objective_instance.is_goal_value_money, objective_instance.show_progress, True)
                    completed_objectives = []
                    if value >= objective_instance.goal_value():
                        if not aspiration_tracker.objective_completed(objective_instance):
                            aspiration_tracker.complete_objective(objective_instance, aspiration_instance)
                            completed_objectives.append(objective_instance)
                    self._try_complete_milestone(sim_info, aspiration_instance, objective_instances=completed_objectives)
                elif objective_instance.data_type == ObjectiveDataStorageType.IdData:
                    value = set(value)
                    aspiration_tracker.data_object.set_objective_value(objective_instance, value)
                    objective_count = aspiration_tracker.data_object.get_objective_count(objective_instance)
                    aspiration_tracker.update_objective(objective_instance, objective_count, objective_instance.goal_value(), objective_instance.is_goal_value_money, objective_instance.show_progress, True)
                    completed_objectives = []
                    if objective_count >= objective_instance.goal_value():
                        if not aspiration_tracker.objective_completed(objective_instance):
                            aspiration_tracker.complete_objective(objective_instance, aspiration_instance)
                            completed_objectives.append(objective_instance)
                    self._try_complete_milestone(sim_info, aspiration_instance, objective_instances=completed_objectives)

    @sim_info_required(default=False)
    def complete_aspiration_objective(self, aspiration_id, objective_id):
        sim_info = self.get_sim_info()
        aspiration_tracker = sim_info.aspiration_tracker
        if aspiration_tracker is not None:
            aspiration_instance = get_resource_service().get_instance(OmutsuResourceType.ASPIRATION, aspiration_id)
            objective_instance = get_resource_service().get_instance(OmutsuResourceType.OBJECTIVE, objective_id)
            if aspiration_instance is not None and objective_instance is not None:
                if not aspiration_tracker.objective_completed(objective_instance):
                    aspiration_tracker.update_objective(objective_instance, objective_instance.goal_value(), objective_instance.goal_value(), objective_instance.is_goal_value_money, objective_instance.show_progress, True)
                    aspiration_tracker.complete_objective(objective_instance, aspiration_instance)
                    self._try_complete_milestone(sim_info, aspiration_instance, objective_instances=(objective_instance,))

    @sim_info_required()
    def reset_aspiration_objective(self, objective_id):
        sim_info = self.get_sim_info()
        aspiration_tracker = sim_info.aspiration_tracker
        if aspiration_tracker is not None:
            objective_instance = get_resource_service().get_instance(OmutsuResourceType.OBJECTIVE, objective_id)
            if objective_instance is not None:
                if aspiration_tracker.objective_completed(objective_instance):
                    aspiration_tracker._try_reset_objective(objective_instance)
                    aspiration_tracker._send_objectives_update_to_client()

    @sim_info_required()
    def reset_all_aspiration_objectives(self, aspiration_id):
        sim_info = self.get_sim_info()
        aspiration_tracker = sim_info.aspiration_tracker
        if aspiration_tracker is not None:
            aspiration_instance = get_resource_service().get_instance(OmutsuResourceType.ASPIRATION, aspiration_id)
            if aspiration_instance is not None:
                aspiration_tracker.reset_milestone(aspiration_instance)
                aspiration_tracker._send_objectives_update_to_client()

    def _try_complete_milestone(self, sim_info, aspiration_instance, objective_instances=()):
        aspiration_tracker = sim_info.aspiration_tracker
        aspiration_tracker.send_if_dirty()
        if objective_instances:
            aspiration_tracker.update_objectives_after_ui_change(objective_instances)
        if not aspiration_tracker.milestone_completed(aspiration_instance):
            objectives_completed = sum((1 for objective_to_complete in aspiration_tracker.get_objectives(aspiration_instance)))
            if aspiration_tracker.should_milestone_complete(aspiration_instance, objectives_completed):
                aspiration_tracker.complete_milestone(aspiration_instance, sim_info)
                aspiration_tracker.post_completion_ui_update(aspiration_instance, sim_info)
