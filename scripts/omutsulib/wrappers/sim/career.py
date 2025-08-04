from collections import namedtuple
import services
from omutsulib.services.cas_service import OmutsuOutfitCategory
from omutsulib.wrappers.enum import OmutsuIntEnum
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class OmutsuCareerCategory(OmutsuIntEnum):
    INVALID = 0
    WORK = 1
    SCHOOL = 2
    TEEN_PARTTIME = 3
    VOLUNTEER = 4
    ADULT_PARTTIME = 5
    UNIVERSITY_COURSE = 6
    TEEN_SIDE_HUSTLE = 7


class OmutsuBusinessEmployeeType(OmutsuIntEnum):
    RETAIL = 1
    RESTAURANT_CHEF = 2
    RESTAURANT_WAITSTAFF = 3
    RESTAURANT_HOST = 4
    VET = 5


_CareerData = namedtuple("_CareerData", ('level', 'max_level'))

class _OmutsuSimCareerMixin(_SuperOmutsuSim):

    @sim_info_required(default=False)
    def quit_career(self, career_id, display_message=True):
        sim_info = self.get_sim_info()
        if sim_info.career_tracker is not None:
            for career_uid, career_instance in sim_info.career_tracker.get_quittable_careers().items():
                if career_instance.guid64 == career_id:
                    sim_info.career_tracker.remove_career(career_uid, post_quit_msg=display_message)
                    return True

        return False

    @sim_info_required(default=False)
    def has_career(self, career_id=None, category=None):
        sim_info = self.get_sim_info()
        if sim_info.career_tracker is not None:
            if career_id is not None:
                return any((career.guid64 == career_id for career in sim_info.career_tracker))
            if category is not None:
                return any((career.career_category == category for career in sim_info.career_tracker))
            return sim_info.career_tracker.has_career
        return False

    @sim_info_required(default=())
    def get_careers(self):
        sim_info = self.get_sim_info()
        if sim_info.career_tracker is not None:
            return tuple((career.guid64 for career in sim_info.career_tracker))
        return ()

    @sim_info_required(default=())
    def get_career_data(self, career_id) -> _CareerData:
        sim_info = self.get_sim_info()
        if sim_info.career_tracker is not None:
            career = next(iter((_career for _career in sim_info.career_tracker)), None)
            if career is not None:
                return _CareerData(career.level, len(career._current_track.career_levels))

    @sim_info_required(default=False)
    def is_current_at_work(self):
        sim_info = self.get_sim_info()
        if sim_info.career_tracker is not None:
            if sim_info.career_tracker.get_currently_at_work_career() is not None:
                return True
            return False

    @sim_info_required(default=False)
    def is_current_work_outfit_category_and_index(self):
        sim_info = self.get_sim_info()
        if sim_info.career_tracker is not None:
            career = sim_info.career_tracker.get_currently_at_work_career()
            if career is not None:
                outfit_index = career.outfit_index or 0
                return (
                 OmutsuOutfitCategory.CAREER, outfit_index)

    @sim_info_required(default=False)
    def is_career_busy(self, pre_work=False):
        sim_info = self.get_sim_info()
        if sim_info.career_tracker is not None:
            current_time = services.time_service().sim_now
            current_time_in_ticks = current_time.time_since_beginning_of_week().absolute_ticks()
            for career in sim_info.career_tracker:
                busy_times = career.get_busy_time_periods()
                for (busy_start_time, busy_end_time) in busy_times:
                    if not pre_work:
                        if current_time_in_ticks >= busy_start_time and current_time_in_ticks <= busy_end_time:
                            return True
                        else:
                            if abs(current_time_in_ticks - busy_start_time) < 45000:
                                return True

        return False

    @sim_info_required(default=False)
    def get_career_performance(self, career_id):
        sim_info = self.get_sim_info()
        if sim_info.career_tracker is not None:
            for career in sim_info.career_tracker:
                if career.guid64 == career_id:
                    return career.work_performance

        return 0

    @sim_info_required(default=False)
    def change_career_performance(self, career_id, amount):
        sim_info = self.get_sim_info()
        if sim_info.career_tracker is not None:
            for career in sim_info.career_tracker:
                if career.guid64 == career_id:
                    career.add_work_performance(amount)
                    career.resend_career_data()
                    return True

        return False
