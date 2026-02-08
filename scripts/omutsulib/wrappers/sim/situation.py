import services
from omutsulib.wrappers.enum import OmutsuIntFlagsEnum
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class OmutsuBouncerExclusivityCategory(OmutsuIntFlagsEnum):
    LEAVE = 2
    NORMAL = 4
    WALKBY = 8
    SERVICE = 16
    VISIT = 32
    LEAVE_NOW = 64
    UNGREETED = 128
    PRE_VISIT = 256
    WORKER = 512
    NEUTRAL = 1024
    VENUE_EMPLOYEE = 2048
    VENUE_BACKGROUND = 4096
    CLUB_GATHERING = 8192
    FESTIVAL_BACKGROUND = 16384
    FESTIVAL_GOER = 32768
    WALKBY_SNATCHER = 65536
    CAREGIVER = 131072
    FIRE = 262144
    NON_WALKBY_BACKGROUND = 524288
    VENUE_GOER = 1048576
    SQUAD = 2097152
    INFECTED = 4194304
    NEUTRAL_UNPOSSESSABLE = 8388608
    NORMAL_UNPOSSESSABLE = 16777216


class _OmutsuSimSituationMixin(_SuperOmutsuSim):

    def end_situation(self, *situation_ids):
        sim = self.get_sim_instance()
        if sim is None:
            return False
        situation_ids = set(situation_ids)
        for situation in services.get_zone_situation_manager().get_situations_sim_is_in(sim):
            if situation.guid64 in situation_ids:
                situation._self_destruct()

        return True

    def has_situation(self, *situation_ids):
        sim = self.get_sim_instance()
        if sim is None:
            return False
        sim_situation_ids = {situation.guid64 for situation in services.get_zone_situation_manager().get_situations_sim_is_in(sim)}
        return not set(situation_ids).isdisjoint(sim_situation_ids)

    def get_running_situations(self):
        sim = self.get_sim_instance()
        if sim is None:
            return ()
        return services.get_zone_situation_manager().get_situations_sim_is_in(sim)

    def get_running_situations_with_job_role(self):
        sim = self.get_sim_instance()
        if sim is None:
            return ()
        situations_with_jobs = []
        for situation in services.get_zone_situation_manager().get_situations_sim_is_in(sim):
            situations_with_jobs.append((situation, situation.get_current_job_for_sim(sim), situation.get_current_role_state_for_sim(sim)))

        return situations_with_jobs

    def has_situation_job(self, *situation_job_ids):
        sim = self.get_sim_instance()
        if sim is None:
            return False
        situation_job_ids = set(situation_job_ids)
        return any((any((situation_job.guid64 in situation_job_ids for situation_job in situation.all_jobs_gen())) for situation in services.get_zone_situation_manager().get_situations_sim_is_in(sim)))

    def has_situation_tag(self, *tags):
        sim = self.get_sim_instance()
        if sim is None:
            return False
        tags = set(tags)
        for situation in services.get_zone_situation_manager().get_situations_sim_is_in(sim):
            if situation.tags & tags:
                return True
            else:
                for situation_job in situation.all_jobs_gen():
                    if situation_job.tags & tags:
                        return True

                role_state = situation.get_current_role_state_for_sim(sim)
            if role_state is not None:
                if role_state.tags & tags:
                    return True

        return False

    def has_exclusivity_situation_of_type(self, *bouncer_exclusivity_categories):
        sim = self.get_sim_instance()
        if sim is None:
            return False
        return any((situation.exclusivity in bouncer_exclusivity_categories for situation in services.get_zone_situation_manager().get_situations_sim_is_in(sim)))

    def create_visit_situation(self, situation_type_override=None):
        sim = self.get_sim_instance()
        if sim is None:
            return False
        return services.get_zone_situation_manager().create_visit_situation(sim, visit_type_override=situation_type_override)

    def initiate_leave_situation(self, must_run=False):
        sim = self.get_sim_instance()
        if sim is None:
            return False
        services.get_zone_situation_manager().make_sim_leave(sim)
        if must_run:
            services.get_zone_situation_manager().make_sim_leave_now_must_run(sim)

    @sim_info_required()
    def clear_goodbye_notification(self):
        self.get_sim_info().clear_goodbye_notification()
