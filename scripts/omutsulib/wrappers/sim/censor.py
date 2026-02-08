from omutsulib.services.components_service import get_components_service, OmutsuComponentType
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim

class OmutsuCensorType:
    OFF = 3188902525
    TORSO = 3465735571
    TORSO_PELVIS = 2022575029
    PELVIS = 2484305261
    TODDLER_PELVIS = 1215676254
    FULLBODY = 958941257
    RIGHT_HAND = 90812611
    LEFT_HAND = 2198569869
    FACE = 2975202225


class _OmutsuSimCensorMixin(_SuperOmutsuSim):

    def add_censor(self, censor_type):
        sim = self.get_sim_instance()
        if sim is not None:
            censorship_component = get_components_service().get_object_component(sim, OmutsuComponentType.CENSOR_GRID)
            if censorship_component is not None:
                return censorship_component.add_censor(censor_type)
            return -1

    def remove_censor(self, handle_id):
        sim = self.get_sim_instance()
        if sim is not None:
            censorship_component = get_components_service().get_object_component(sim, OmutsuComponentType.CENSOR_GRID)
            if censorship_component is not None:
                if handle_id in censorship_component._censor_grid_handles:
                    censorship_component.remove_censor(handle_id)
