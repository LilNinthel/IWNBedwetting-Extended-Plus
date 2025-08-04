from typing import TYPE_CHECKING
import services
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required
if TYPE_CHECKING:
    from omutsulib.wrappers.sim.sim import OmutsuSim

class _OmutsuSimClubMixin(_SuperOmutsuSim):

    def is_at_club_gathering(self):
        sim = self.get_sim_instance()
        if sim is not None:
            club_service = services.get_club_service()
            if club_service is not None:
                if sim in club_service.sims_to_gatherings_map:
                    return True
            return False

    @sim_info_required(default=(None, None))
    def get_current_club_gathering(self):
        club_service = services.get_club_service()
        if club_service is not None:
            sim_clubs = club_service.get_clubs_for_sim_info(self.get_sim_info())
            for club in sim_clubs:
                club_gathering = club_service.clubs_to_gatherings_map.get(club)
                if club_gathering is not None:
                    return (club, club_gathering)

        return (None, None)

    @sim_info_required(default=((), ()))
    def get_club_outfit_parts(self, club, outfit_category_and_index):
        sim_info = self.get_sim_info()
        return club.get_club_outfit_parts(sim_info, outfit_category_and_index)

    @sim_info_required(default=False, base_wrapper=True)
    def remove_club_appearance_modifiers(self: "OmutsuSim", club_gathering=None):
        if club_gathering is None:
            (_, club_gathering) = self.get_current_club_gathering()
        if club_gathering is not None:
            self.remove_appearance_modifiers(club_gathering.guid)
            self.unregister_on_outfit_changed_callback(club_gathering._on_outfit_removed)
