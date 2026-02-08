import services
from objects import HiddenReasonFlag
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class _OmutsuSimWorldMixin(_SuperOmutsuSim):

    def is_at_active_lot(self):
        sim = self.get_sim_instance()
        if sim is not None:
            return services.active_lot().is_position_on_lot(sim.position)
        return False

    @sim_info_required(default=False)
    def is_active_lot_owner(self, allow_rental=True, allow_business=True):
        sim_info = self.get_sim_info()
        current_zone = services.current_zone()
        if sim_info.household is not None:
            if sim_info.household.home_zone_id == current_zone.id:
                return True
            if allow_rental:
                if sim_info.is_renting_zone(current_zone.id):
                    return True
                if allow_business:
                    if current_zone.lot is not None:
                        if current_zone.lot.zone_owner_household_id == sim_info.household_id:
                            return True
            return False

    def is_at_rabbit_hole(self):
        sim = self.get_sim_instance()
        if sim is not None:
            return sim.has_hidden_flags(HiddenReasonFlag.RABBIT_HOLE)
        return False

    def is_leaving_zone(self):
        sim = self.get_sim_instance()
        if sim is not None:
            return services.sim_spawner_service().sim_is_leaving(sim)
        return False
