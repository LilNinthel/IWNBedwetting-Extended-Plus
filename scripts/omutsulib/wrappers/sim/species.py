from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class OmutsuSpecies:
    INVALID = 0
    HUMAN = 1
    DOG = 2
    CAT = 3
    FOX = 5
    HORSE = 6


class _OmutsuSimSpeciesMixin(_SuperOmutsuSim):

    @sim_info_required(default=(OmutsuSpecies.INVALID), base_wrapper=True)
    def get_species(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return sim_info.species

    @sim_info_required(base_wrapper=True)
    def set_species(self, species):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info.species = species

    def is_human(self):
        return self.get_species() == OmutsuSpecies.HUMAN

    def is_pet(self):
        return self.get_species() != OmutsuSpecies.HUMAN
