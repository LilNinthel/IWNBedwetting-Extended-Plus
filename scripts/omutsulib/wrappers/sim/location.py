from world.ocean_tuning import OceanTuning
from omutsulib.utils.math import Location, SurfaceIdentifier
from omutsulib.utils.singletons import ZERO_VECTOR3, ZERO_TRANSFORM
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim

class _OmutsuSimLocationMixin(_SuperOmutsuSim):

    def set_location(self, location):
        sim = self.get_sim_instance()
        if sim is not None:
            sim.location = location

    def get_location(self):
        sim = self.get_sim_instance()
        if sim is not None:
            return sim.location
        return Location(ZERO_VECTOR3, 0, 0.0)

    def get_transform(self):
        sim = self.get_sim_instance()
        if sim is not None:
            return sim.transform
        return ZERO_TRANSFORM

    def get_position(self, bone_name=None):
        sim = self.get_sim_instance()
        if sim is not None:
            if bone_name is not None:
                try:
                    return sim.get_joint_transform_for_joint(bone_name).translation
                except:
                    pass

                return sim.position
            return ZERO_VECTOR3

    def get_forward_vector(self):
        sim = self.get_sim_instance()
        if sim is not None:
            return sim.forward
        return ZERO_VECTOR3

    def get_orientation(self):
        sim = self.get_sim_instance()
        if sim is not None:
            return sim.orientation
        return 0.0

    def get_routing_surface(self):
        sim = self.get_sim_instance()
        if sim is not None:
            return sim.routing_surface
        return SurfaceIdentifier(0)

    def get_level(self):
        sim = self.get_sim_instance()
        if sim is not None:
            if sim.routing_surface:
                return sim.routing_surface.secondary_id
            return 0
        return 0

    def get_wading_bounds(self):
        sim = self.get_sim_instance()
        if sim is not None:
            wading_interval = OceanTuning.get_actor_wading_interval(sim)
            if wading_interval is not None:
                return (wading_interval.lower_bound, wading_interval.upper_bound)
            return (0, 0)

    def can_swim_at_location(self, location):
        sim = self.get_sim_instance()
        if sim is not None:
            return sim.should_be_swimming_at_position(location.transform.translation, location.level)
        return False

    def get_intended_location(self):
        sim = self.get_sim_instance()
        if sim is not None:
            return Location((self.get_intended_position()), 0, 0, surface_override=(self.get_intended_routing_surface()))
        return Location(ZERO_VECTOR3, 0, 0.0)

    def get_intended_position(self):
        sim = self.get_sim_instance()
        if sim is not None:
            return sim.intended_transform.translation
        return ZERO_VECTOR3

    def get_intended_routing_surface(self):
        sim = self.get_sim_instance()
        if sim is not None:
            return sim.intended_routing_surface
        return SurfaceIdentifier(0)
