from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class _OmutsuSimGeneticMixin(_SuperOmutsuSim):

    @sim_info_required(default=False)
    def apply_genetics(self, parent_a_identifier, parent_b_identifier, seed=1, **kwargs):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        from omutsulib.wrappers.sim.sim import OmutsuSim
        parent_a_omutsu_sim = OmutsuSim(parent_a_identifier)
        parent_b_omutsu_sim = OmutsuSim(parent_b_identifier)
        if parent_a_omutsu_sim is not None:
            if parent_b_omutsu_sim is not None:
                (sim_info.apply_genetics)(parent_a_omutsu_sim.get_sim_info(), parent_b_omutsu_sim.get_sim_info(), seed=seed, **kwargs)
                return True
            return False

    @sim_info_required(default=False)
    def apply_parents_relations(self, parent_a_identifier, parent_b_identifier):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        from omutsulib.wrappers.sim.sim import OmutsuSim
        parent_a_omutsu_sim = OmutsuSim(parent_a_identifier)
        parent_b_omutsu_sim = OmutsuSim(parent_b_identifier)
        if parent_a_omutsu_sim is not None:
            if parent_b_omutsu_sim is not None:
                sim_info.add_parent_relations(parent_a_omutsu_sim.get_sim_info(), parent_b_omutsu_sim.get_sim_info())
                return True
            return False
