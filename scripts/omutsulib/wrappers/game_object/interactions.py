from omutsulib.services.components_service import get_components_service, OmutsuComponentType
from omutsulib.services.resources_service import get_resource_service, OmutsuResourceType
from omutsulib.wrappers.game_object.super_game_object import _SuperOmutsuGameObject

class _OmutsuObjectInteractionsMixin(_SuperOmutsuGameObject):

    def add_super_affordances(self, *affordances):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            affordance_manager = get_resource_service().get_instance_manager(OmutsuResourceType.INTERACTION)
            affordance_instances = []
            for affordance_id in affordances:
                affordance_instance = get_resource_service().get_instance_from_manager(affordance_manager, affordance_id)
                if affordance_instance is not None:
                    if affordance_instance not in object_instance._super_affordances:
                        affordance_instances.append(affordance_instance)

            if affordance_instances:
                object_instance._super_affordances += tuple(affordance_instances)

    def get_super_affordances(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance._super_affordances
        return ()

    def is_sim_locked(self, sim_identifier):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            object_locking_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.OBJECT_LOCKING)
            if object_locking_component is not None:
                from omutsulib.wrappers.sim.sim import OmutsuSim
                omutsu_sim = OmutsuSim(sim_identifier)
                if omutsu_sim is not None:
                    if object_locking_component.test_lock(omutsu_sim.get_sim_instance()):
                        return True
            return False
