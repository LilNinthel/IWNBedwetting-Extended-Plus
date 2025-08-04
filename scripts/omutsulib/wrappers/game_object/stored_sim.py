from typing import TYPE_CHECKING
from omutsulib.services.components_service import get_components_service, OmutsuComponentType
from omutsulib.wrappers.game_object.super_game_object import _SuperOmutsuGameObject
if TYPE_CHECKING:
    from omutsulib.wrappers.sim.sim import OmutsuSim

class _OmutsuObjectStoredSimMixin(_SuperOmutsuGameObject):

    def get_stored_sims(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            store_sim_info_component = get_components_service().get_object_component(object_instance, (OmutsuComponentType.STORED_SIM_INFO), add_dynamic=True)
            if store_sim_info_component is not None:
                stored_omutsu_sims = []
                from omutsulib.wrappers.sim.sim import OmutsuSim
                for sim_id in store_sim_info_component.get_stored_sim_id_list():
                    omutsu_sim = OmutsuSim(sim_id)
                    if omutsu_sim is not None:
                        stored_omutsu_sims.append(omutsu_sim)

                return stored_omutsu_sims
            return ()

    def add_stored_sim(self, omutsu_sim: "OmutsuSim"):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            store_sim_info_component = get_components_service().get_object_component(object_instance, (OmutsuComponentType.STORED_SIM_INFO), add_dynamic=True)
            if store_sim_info_component is not None:
                store_sim_info_component.add_sim_id_to_list(omutsu_sim.get_sim_id())
