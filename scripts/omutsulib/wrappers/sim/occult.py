from sims.occult.occult_enums import OccultType
from omutsulib.native_enums.traits import NativeTrait
from omutsulib.wrappers.enum import OmutsuIntFlagsEnum
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required
from omutsulib.wrappers.sim.traits import OmutsuTraitType

class OmutsuOccultType(OmutsuIntFlagsEnum):
    HUMAN = 1
    ALIEN = 2
    VAMPIRE = 4
    MERMAID = 8
    WITCH = 16
    WEREWOLF = 32
    FAIRY = 64


class ExtendedOmutsuOccultType(OmutsuOccultType):
    SUCCUBUS = 1024


class _OmutsuSimOccultMixin(_SuperOmutsuSim):
    _SKELETON_TRAITS = {
     175972, 177810, 178437, 253237}

    @sim_info_required(default=(OmutsuOccultType.HUMAN), base_wrapper=True)
    def get_current_occult_type(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return OccultType(sim_info._base.current_occult_types)

    @sim_info_required(default=(OmutsuOccultType.HUMAN,))
    def get_occult_types(self):
        occult_types = set()
        for occult_type in OccultType:
            if self.get_sim_info().occult_tracker.has_occult_type(occult_type):
                occult_types.add(occult_type)

        return occult_types

    @sim_info_required()
    def get_occult_omutsu_sim(self, occult_type, fallback_to_base=True):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        sim_info = self.get_sim_info()
        occult_sim_info = sim_info.occult_tracker.get_occult_sim_info(occult_type)
        if occult_sim_info is not None:
            return OmutsuSim(occult_sim_info, sim_id=(sim_info.sim_id), exclusive_base_wrapper=True)
        if fallback_to_base:
            return OmutsuSim(sim_info)

    @sim_info_required(default=())
    def get_all_occult_omutsu_sims(self, include_base=True):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        sim_info = self.get_sim_info()
        occult_sim_info_list = []
        if include_base:
            occult_sim_info_list.append(OmutsuSim(sim_info))
        for occult_type in OccultType:
            occult_sim_info = sim_info.occult_tracker.get_occult_sim_info(occult_type)
            if occult_sim_info is not None:
                occult_sim_info_list.append(OmutsuSim(occult_sim_info, sim_id=(sim_info.sim_id), exclusive_base_wrapper=True))

        return occult_sim_info_list

    @sim_info_required(default=False)
    def is_alien(self):
        return any((trait.guid64 == NativeTrait.OCCULT_ALIEN for trait in self.get_sim_info().trait_tracker.equipped_traits))

    @sim_info_required(default=False)
    def is_vampire(self):
        return any((trait.guid64 == NativeTrait.OCCULT_VAMPIRE for trait in self.get_sim_info().trait_tracker.equipped_traits))

    @sim_info_required(default=False)
    def is_mermaid(self):
        return any((trait.guid64 == NativeTrait.OCCULT_MERMAID for trait in self.get_sim_info().trait_tracker.equipped_traits))

    @sim_info_required(default=False)
    def is_witch(self):
        return any((trait.guid64 == NativeTrait.OCCULT_WITCH_OCCULT for trait in self.get_sim_info().trait_tracker.equipped_traits))

    @sim_info_required(default=False)
    def is_werewolf(self):
        return any((trait.guid64 == NativeTrait.OCCULT_WEREWOLF for trait in self.get_sim_info().trait_tracker.equipped_traits))

    @sim_info_required(default=False)
    def is_fairy(self):
        return any((trait.guid64 == NativeTrait.OCCULT_FAIRY_ALL_AGES for trait in self.get_sim_info().trait_tracker.equipped_traits))

    @sim_info_required(default=False)
    def is_plantsim(self):
        return any((trait.guid64 == NativeTrait.PLANT_SIM for trait in self.get_sim_info().trait_tracker.equipped_traits))

    @sim_info_required(default=False)
    def is_skeleton(self):
        return any((trait.guid64 in self._SKELETON_TRAITS for trait in self.get_sim_info().trait_tracker.equipped_traits))

    @sim_info_required(default=False)
    def is_ghost(self):
        return any((trait.trait_type == OmutsuTraitType.GHOST for trait in self.get_sim_info().trait_tracker.equipped_traits))

    @sim_info_required(default=False)
    def is_robot(self):
        return any((trait.trait_type == OmutsuTraitType.ROBOT for trait in self.get_sim_info().trait_tracker.equipped_traits))

    @sim_info_required(default=False)
    def is_batuu_alien(self):
        return any((trait.trait_type == OmutsuTraitType.BATUU_ALIEN for trait in self.get_sim_info().trait_tracker.equipped_traits))
