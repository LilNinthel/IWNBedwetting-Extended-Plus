from sims.pregnancy.pregnancy_tracker import PregnancyTracker
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class OmutsuPregnancyOrigin:
    DEFAULT = 0
    ALIEN_ABDUCTION = 64
    VAMPIRE_BATS = 65
    LIGHTHOUSE = 66
    FATHER_WINTER = 67
    MONEY_PILE = 68
    MERFOLK = 69
    ELEMENTAL = 70


class _OmutsuSimPregnancyMixin(_SuperOmutsuSim):

    @sim_info_required(default=False)
    def is_pregnant(self):
        pregnancy_tracker = self.get_sim_info().pregnancy_tracker
        if pregnancy_tracker is not None:
            return pregnancy_tracker.is_pregnant
        return False

    @sim_info_required(default=0)
    def get_pregnancy_progress(self):
        sim_info = self.get_sim_info()
        pregnancy_tracker = sim_info.pregnancy_tracker
        if pregnancy_tracker is not None and pregnancy_tracker.is_pregnant:
            pregnancy_commodity_type = pregnancy_tracker.PREGNANCY_COMMODITY_MAP.get(sim_info.species)
            statistic_tracker = sim_info.get_tracker(pregnancy_commodity_type)
            pregnancy_commodity = statistic_tracker.get_statistic(pregnancy_commodity_type, add=False)
            if pregnancy_commodity:
                return pregnancy_commodity.get_value()
            return 0

    def get_pregnancy_rate(self):
        return PregnancyTracker.PREGNANCY_RATE

    @sim_info_required(default=False)
    def start_pregnancy(self, partner_sim_identifier, pregnancy_origin=OmutsuPregnancyOrigin.DEFAULT, single_sim_is_allowed=False):
        sim_info = self.get_sim_info()
        from omutsulib.wrappers.sim.sim import OmutsuSim
        partner_sim = OmutsuSim(partner_sim_identifier)
        if partner_sim is None:
            return False
        household = sim_info.household
        if household is not None:
            pregnancy_tracker = sim_info.pregnancy_tracker
            if pregnancy_tracker is not None:
                if household.free_slot_count <= 0:
                    return False
                pregnancy_tracker.start_pregnancy(sim_info, (partner_sim.get_sim_info()), pregnancy_origin=pregnancy_origin, single_sim_is_allowed=single_sim_is_allowed)
                pregnancy_tracker.clear_pregnancy_visuals()
                from omutsulib.services.statistics_service import get_statistics_service
                get_statistics_service().set_statistic_value(sim_info, 16640, 1)
                return True
            return False

    @sim_info_required(default=None)
    def get_pregnancy_partner_sim(self):
        pregnancy_tracker = self.get_sim_info().pregnancy_tracker
        if pregnancy_tracker is not None:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            return OmutsuSim(pregnancy_tracker.get_partner())

    @sim_info_required()
    def create_pregnancy_offspring_data(self):
        pregnancy_tracker = self.get_sim_info().pregnancy_tracker
        if pregnancy_tracker is not None:
            pregnancy_tracker.create_offspring_data()

    @sim_info_required()
    def get_pregnancy_offspring_data_gen(self):
        pregnancy_tracker = self.get_sim_info().pregnancy_tracker
        if pregnancy_tracker is not None:
            yield from pregnancy_tracker.get_offspring_data_gen()
        if False:
            yield None

    @sim_info_required(default=False)
    def clear_pregnancy(self):
        pregnancy_tracker = self.get_sim_info().pregnancy_tracker
        if pregnancy_tracker is not None:
            self.get_sim_info().pregnancy_tracker.clear_pregnancy()
            return True
        return False
