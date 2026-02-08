import services
from omutsulib.wrappers.household import OmutsuHousehold
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class _OmutsuSimHouseholdMixin(_SuperOmutsuSim):

    @sim_info_required(default=False)
    def has_household(self):
        sim_info = self.get_sim_info()
        return sim_info.household is not None

    @sim_info_required(default=0)
    def get_household_id(self):
        sim_info = self.get_sim_info()
        if sim_info.household is not None:
            return sim_info.household.id
        return 0

    @sim_info_required(default=None)
    def get_omutsu_household(self) -> OmutsuHousehold:
        sim_info = self.get_sim_info()
        if sim_info.household is not None:
            return OmutsuHousehold(sim_info.household)

    @sim_info_required(default=False)
    def is_at_home(self):
        sim = self.get_sim_instance()
        if sim is not None:
            if sim.household is not None:
                return sim.on_home_lot
            return False

    @sim_info_required(default=False)
    def is_roommate(self, household_id=None):
        roommate_service = services.get_roommate_service()
        if roommate_service is not None:
            return roommate_service.is_sim_info_roommate(self.get_sim_info(), household_id)
        return False
