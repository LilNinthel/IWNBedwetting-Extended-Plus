from omutsulib.wrappers.sim.age import _OmutsuSimAgeMixin
from omutsulib.wrappers.sim.aspirations import _OmutsuSimAspirationsMixin
from omutsulib.wrappers.sim.autonomy import _OmutsuSimAutonomyMixin
from omutsulib.wrappers.sim.buffs import _OmutsuSimBuffMixin
from omutsulib.wrappers.sim.career import _OmutsuSimCareerMixin
from omutsulib.wrappers.sim.carry import _OmutsuSimCarryMixin
from omutsulib.wrappers.sim.cas import _OmutsuSimCASMixin, _OmutsuSimAppearanceModifiersMixin, _OmutsuSimAppearanceAttributesMixin
from omutsulib.wrappers.sim.censor import _OmutsuSimCensorMixin
from omutsulib.wrappers.sim.club import _OmutsuSimClubMixin
from omutsulib.wrappers.sim.diaper import _OmutsuSimDiaperMixin
from omutsulib.wrappers.sim.gender import _OmutsuSimGenderMixin
from omutsulib.wrappers.sim.genetics import _OmutsuSimGeneticMixin
from omutsulib.wrappers.sim.household import _OmutsuSimHouseholdMixin
from omutsulib.wrappers.sim.interactions import _OmutsuSimInteractionMixin
from omutsulib.wrappers.sim.internal import _OmutsuSimInternalMixin
from omutsulib.wrappers.sim.inventory import _OmutsuSimInventoryMixin
from omutsulib.wrappers.sim.location import _OmutsuSimLocationMixin
from omutsulib.wrappers.sim.name import _OmutsuSimNameMixin
from omutsulib.wrappers.sim.occult import _OmutsuSimOccultMixin
from omutsulib.wrappers.sim.pacifier import _OmutsuSimPacifierMixin
from omutsulib.wrappers.sim.pregnancy import _OmutsuSimPregnancyMixin
from omutsulib.wrappers.sim.relationship import _OmutsuSimRelationshipMixin
from omutsulib.wrappers.sim.situation import _OmutsuSimSituationMixin
from omutsulib.wrappers.sim.species import _OmutsuSimSpeciesMixin
from omutsulib.wrappers.sim.statistics import _OmutsuSimStatisticsMixin, _OmutsuSimSkillsMixin
from omutsulib.wrappers.sim.super_sim import OmutsuSimSingleton
from omutsulib.wrappers.sim.traits import _OmutsuSimTraitMixin
from omutsulib.wrappers.sim.travel import _OmutsuSimTravelMixin
from omutsulib.wrappers.sim.whim import _OmutsuSimWhimMixin
from omutsulib.wrappers.sim.world import _OmutsuSimWorldMixin


class OmutsuSim(_OmutsuSimDiaperMixin, _OmutsuSimPacifierMixin, _OmutsuSimInternalMixin, _OmutsuSimNameMixin, _OmutsuSimSpeciesMixin, _OmutsuSimGenderMixin, _OmutsuSimAgeMixin, _OmutsuSimOccultMixin, _OmutsuSimHouseholdMixin, _OmutsuSimTraitMixin, _OmutsuSimBuffMixin, _OmutsuSimInteractionMixin, _OmutsuSimWorldMixin, _OmutsuSimPregnancyMixin, _OmutsuSimCASMixin, _OmutsuSimAppearanceModifiersMixin, _OmutsuSimAppearanceAttributesMixin, _OmutsuSimLocationMixin, _OmutsuSimRelationshipMixin, _OmutsuSimInventoryMixin, _OmutsuSimAutonomyMixin, _OmutsuSimTravelMixin, _OmutsuSimClubMixin, _OmutsuSimStatisticsMixin, _OmutsuSimSkillsMixin, _OmutsuSimSituationMixin, _OmutsuSimCensorMixin, _OmutsuSimCareerMixin, _OmutsuSimWhimMixin, _OmutsuSimAspirationsMixin, _OmutsuSimGeneticMixin,  _OmutsuSimCarryMixin, metaclass=OmutsuSimSingleton):

    def __init__(self, *args, sim_id=0, exclusive_base_wrapper=False):
        sim_identifier = args[0]
        super().__init__(sim_identifier, sim_id=sim_id, exclusive_base_wrapper=exclusive_base_wrapper)

    def __repr__(self):
        return "{} {}".format(self.get_first_name(), self.get_last_name())
