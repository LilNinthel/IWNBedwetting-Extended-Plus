from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim

class _OmutsuSimCarryMixin(_SuperOmutsuSim):

    def get_carry_object_instances_gen(self):
        sim = self.get_sim_instance()
        if sim is not None:
            if sim.posture_state is not None:
                for aspect in sim.posture_state.carry_aspects:
                    if aspect.target is not None:
                        yield aspect.target
