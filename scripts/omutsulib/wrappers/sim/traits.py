from omutsulib.services.resources_service import get_resource_service, OmutsuResourceType
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class OmutsuTraitType:
    PERSONALITY = 0
    GAMEPLAY = 1
    WALKSTYLE = 2
    HIDDEN = 4
    GHOST = 5
    ASPIRATION = 6
    TAILSTYLE = 7
    GENDER_OPTIONS = 8
    SIM_PHONE = 9
    PHASE = 10
    AGENT = 11
    INFECTION = 12
    CURSE = 13
    ROOMMATE = 14
    ROBOT_MODULE = 15
    ROBOT = 16
    PROFESSOR = 17
    UNIVERSITY_DEGREE = 18
    ROBOT_MODULE_LOCKED = 19
    BATUU_ALIEN = 20
    LIFESTYLE = 21
    LIKE = 22
    DISLIKE = 23
    FOOD_RESTRICTION = 24
    TRADITION = 25
    TEMPERAMENT = 26
    PACK_MEMBER = 27
    PACK_FRIEND = 28
    FEAR = 29
    HIGH_SCHOOL = 30
    GAMEPLAY_OBJECT_PREFERENCE = 31
    INFANT_CARRIER = 32
    GAMEPLAY_GENERIC = 33
    HORSE_ACCOLADE = 34
    MASTERY_PERK = 35


class _OmutsuSimTraitMixin(_SuperOmutsuSim):

    @sim_info_required(default=False)
    def has_trait(self, *trait_ids):
        sim_trait_ids = {trait.guid64 for trait in self.get_sim_info().get_traits()}
        return not set(trait_ids).isdisjoint(sim_trait_ids)

    @sim_info_required(default=False)
    def has_trait_type(self, trait_type):
        return any((trait.trait_type == trait_type for trait in self.get_sim_info().trait_tracker.equipped_traits))

    @sim_info_required(default=())
    def get_traits(self):
        return [trait for trait in self.get_sim_info().get_traits()]

    @sim_info_required(default=False)
    def add_trait(self, trait_id):
        trait_instance = get_resource_service().get_instance(OmutsuResourceType.TRAIT, trait_id)
        if trait_instance is None:
            return False
        return self.get_sim_info().add_trait(trait_instance)

    @sim_info_required(default=False)
    def remove_trait(self, *trait_ids):
        success = False
        for trait_id in trait_ids:
            trait_instance = get_resource_service().get_instance(OmutsuResourceType.TRAIT, trait_id)
            if trait_instance is not None:
                if self.get_sim_info().remove_trait(trait_instance):
                    success = True

        return success

    @sim_info_required()
    def clear_traits(self):
        sim_info = self.get_sim_info()
        trait_tracker = sim_info.trait_tracker
        if trait_tracker is not None:
            trait_tracker.clear_traits()

    @sim_info_required()
    def resend_motives_list(self):
        sim_info = self.get_sim_info()
        trait_tracker = sim_info.trait_tracker
        if trait_tracker is not None:
            trait_tracker.sort_and_send_commodity_list()
