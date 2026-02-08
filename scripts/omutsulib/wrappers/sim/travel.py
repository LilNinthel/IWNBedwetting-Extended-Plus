import services
from sims.sim_spawner import SimSpawner
from situations.situation_guest_list import SituationGuestList, SituationGuestInfo, SituationInvitationPurpose
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class _OmutsuSimTravelMixin(_SuperOmutsuSim):

    def spawn_instance(self, **kwargs):
        if self.get_sim_instance() is not None:
            return
        try:
            return (SimSpawner.spawn_sim)((self.get_sim_info()), **kwargs)
        except AssertionError:
            return False

    @sim_info_required()
    def travel_to_zone(self, zone_id, traveling_sim_ids=()):
        sim_info = self.get_sim_info()
        zone_proto_buff = services.get_persistence_service().get_zone_proto_buff(zone_id)
        if zone_proto_buff is not None:
            situation_manager = services.get_zone_situation_manager()
            situation = situation_manager.DEFAULT_TRAVEL_SITUATION
            guest_list = situation.get_predefined_guest_list()
            if guest_list is None:
                guest_list = SituationGuestList(invite_only=True, host_sim_id=(sim_info.id))
                default_job = situation.default_job()
                sim_info_manager = services.sim_info_manager()
                for travel_sim_id in traveling_sim_ids:
                    travel_sim_id = int(travel_sim_id)
                    travel_sim_info = sim_info_manager.get(travel_sim_id)
                    if travel_sim_info is not None:
                        guest_info = SituationGuestInfo.construct_from_purpose(travel_sim_id, default_job, SituationInvitationPurpose.INVITED)
                        guest_list.add_guest_info(guest_info)

                guest_info = SituationGuestInfo.construct_from_purpose(sim_info.id, default_job, SituationInvitationPurpose.INVITED)
                guest_list.add_guest_info(guest_info)
            situation_manager.create_situation(situation, guest_list=guest_list, user_facing=False, zone_id=zone_id)

    @sim_info_required(default=0)
    def get_travel_group_id(self):
        return self.get_sim_info().travel_group_id

    @sim_info_required(default=False)
    def is_renting_zone(self):
        return self.get_sim_info().is_renting_zone(services.current_zone_id())
