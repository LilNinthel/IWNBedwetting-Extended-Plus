from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class _OmutsuSimStatisticsMixin(_SuperOmutsuSim):

    @sim_info_required(default=False)
    def has_statistic(self, statistic_id, combined=False):
        if not combined:
            return self._get_statistics_service().has_statistic(self.get_sim_info(), statistic_id)
        return self._get_combined_statistics_service().has_statistic(self.get_sim_info(), statistic_id)

    @sim_info_required()
    def remove_statistic(self, statistic_id, combined=False):
        if not combined:
            self._get_statistics_service().remove_statistic(self.get_sim_info(), statistic_id)
        else:
            self._get_combined_statistics_service().remove_statistic(self.get_sim_info(), statistic_id)

    @sim_info_required()
    def remove_statistics(self, statistics):
        for statistic_id in statistics:
            self.remove_statistic(statistic_id)

    @sim_info_required()
    def clear_statistic(self, statistic_id):
        self._get_statistics_service().clear_statistic(self.get_sim_info(), statistic_id)

    @sim_info_required()
    def set_statistic_value(self, statistic_id, value, add=True, combined=False):
        if not combined:
            self._get_statistics_service().set_statistic_value((self.get_sim_info()), statistic_id, value, add=add)
        else:
            self._get_combined_statistics_service().set_statistic_value((self.get_sim_info()), statistic_id, value, add=add)

    @sim_info_required()
    def change_statistic_value(self, statistic_id, value, add=True):
        self._get_statistics_service().change_statistic_value((self.get_sim_info()), statistic_id, value, add=add)

    @sim_info_required(default=0)
    def get_statistic_value(self, statistic_id, add=False, combined=False, default=0):
        if not combined:
            return self._get_statistics_service().get_statistic_value((self.get_sim_info()), statistic_id, add=add, default=default)
        return self._get_combined_statistics_service().get_statistic_value((self.get_sim_info()), statistic_id, add=add, default=default)

    @sim_info_required(default=False)
    def is_statistic_min(self, statistic_id, add=False, default=0):
        return self._get_statistics_service().get_statistic_value((self.get_sim_info()), statistic_id, add=add, default=default) == self._get_statistics_service().get_min_statistic_value(statistic_id)

    @sim_info_required(default=False)
    def is_statistic_max(self, statistic_id, add=False, default=0):
        return self._get_statistics_service().get_statistic_value((self.get_sim_info()), statistic_id, add=add, default=default) == self._get_statistics_service().get_max_statistic_value(statistic_id)

    @sim_info_required()
    def add_statistic_modifier(self, statistic_id, modifier_value, add=False):
        return self._get_statistics_service().add_statistic_modifier((self.get_sim_info()), statistic_id, modifier_value, add=add)

    @sim_info_required()
    def remove_statistic_modifier(self, statistic_id, modifier_value, add=False):
        return self._get_statistics_service().remove_statistic_modifier((self.get_sim_info()), statistic_id, modifier_value, add=add)

    @sim_info_required()
    def clear_statistic_modifiers(self, statistic_id, add=False):
        return self._get_statistics_service().clear_statistic_modifiers((self.get_sim_info()), statistic_id, add=add)

    @sim_info_required(default=0)
    def get_statistic_decay_rate(self, statistic_id):
        return self._get_statistics_service().get_statistic_decay_rate(self.get_sim_info(), statistic_id)

    @sim_info_required(default=1)
    def get_statistic_decay_rate_modifier(self, statistic_id):
        return self._get_statistics_service().get_statistic_decay_rate_modifier(self.get_sim_info(), statistic_id)

    @sim_info_required(default=False)
    def is_statistic_locked(self, statistic_id):
        return self._get_statistics_service().is_statistic_locked(self.get_sim_info(), statistic_id)

    @sim_info_required(default=0)
    def get_statistic_locked_count(self, statistic_id):
        return self._get_statistics_service().get_statistic_locked_count(self.get_sim_info(), statistic_id)

    @sim_info_required(default=False)
    def lock_statistic(self, statistic_id, **kwargs):
        return (self._get_statistics_service().lock_statistic)((self.get_sim_info()), statistic_id, **kwargs)

    @sim_info_required(default=False)
    def unlock_statistic(self, statistic_id, **kwargs):
        return (self._get_statistics_service().unlock_statistic)((self.get_sim_info()), statistic_id, **kwargs)

    @sim_info_required()
    def add_statistic_watcher(self, callback):
        return self._get_statistics_service().add_statistic_watcher(self.get_sim_info(), callback)

    @sim_info_required()
    def remove_statistic_watcher(self, handle_id):
        self._get_statistics_service().remove_statistic_watcher(self.get_sim_info(), handle_id)

    def _get_statistics_service(self):
        from omutsulib.services.statistics_service import get_statistics_service
        return get_statistics_service()

    def _get_combined_statistics_service(self):
        from omutsulib.services.combined_statistics_service import get_combined_statistics_service
        return get_combined_statistics_service()

    @sim_info_required(default=False)
    def register_on_statistic_removed_callback(self, callback):
        sim_info = self.get_sim_info()
        commodity_tracker = sim_info.commodity_tracker
        if commodity_tracker is not None:
            if commodity_tracker._on_remove_callbacks is None or callback not in commodity_tracker._on_remove_callbacks:
                commodity_tracker.add_on_remove_callback(callback)
                return True
        return False

    @sim_info_required(default=False)
    def unregister_on_statistic_removed_callback(self, callback):
        sim_info = self.get_sim_info()
        commodity_tracker = sim_info.commodity_tracker
        if commodity_tracker is not None:
            commodity_tracker.remove_on_remove_callback(callback)
            return True
        return False


class _OmutsuSimSkillsMixin(_SuperOmutsuSim):

    @sim_info_required(default=False)
    def has_skill(self, skill_id):
        return self._get_skills_service().has_skill(self.get_sim_info(), skill_id)

    @sim_info_required()
    def remove_skill(self, skill_id):
        self._get_skills_service().remove_skill(self.get_sim_info(), skill_id)

    @sim_info_required()
    def set_skill_value(self, skill_id, value, add=True):
        self._get_skills_service().set_skill_value((self.get_sim_info()), skill_id, value, add=add)

    @sim_info_required()
    def set_skill_level(self, skill_id, level, add=True):
        self._get_skills_service().set_skill_level((self.get_sim_info()), skill_id, level, add=add)

    @sim_info_required()
    def set_skill_level_value(self, skill_id, value, add=True):
        self._get_skills_service().set_skill_level_value((self.get_sim_info()), skill_id, value, add=add)

    @sim_info_required()
    def change_skill_value(self, skill_id, value, add=True):
        self._get_skills_service().change_skill_value((self.get_sim_info()), skill_id, value, add=add)

    @sim_info_required()
    def change_skill_level_value(self, skill_id, value, add=True):
        self._get_skills_service().change_skill_level_value((self.get_sim_info()), skill_id, value, add=add)

    @sim_info_required(default=1)
    def get_skill_value(self, skill_id, add=True):
        return self._get_skills_service().get_skill_value((self.get_sim_info()), skill_id, add=add)

    @sim_info_required(default=1)
    def get_skill_level(self, skill_id, add=False):
        return self._get_skills_service().get_skill_level((self.get_sim_info()), skill_id, add=add)

    @sim_info_required(default=0)
    def get_skill_level_value(self, skill_id, add=False):
        return self._get_skills_service().get_skill_level_value((self.get_sim_info()), skill_id, add=add)

    @sim_info_required(default=1.0)
    def get_skill_absolute_level(self, skill_id, add=False):
        return self._get_skills_service().get_skill_absolute_level((self.get_sim_info()), skill_id, add=add)

    @sim_info_required(default=False)
    def has_reached_skill_max_level(self, skill_id):
        return self._get_skills_service().has_reached_skill_max_level(self.get_sim_info(), skill_id)

    def _get_skills_service(self):
        from omutsulib.services.statistics_service import get_skills_service
        return get_skills_service()
