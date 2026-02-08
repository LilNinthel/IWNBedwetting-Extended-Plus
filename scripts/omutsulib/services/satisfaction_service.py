import sims4.collections
from satisfaction.satisfaction_tracker import SatisfactionTracker
from omutsulib.services.resources_service import get_resource_service, OmutsuResourceType
from omutsulib.services.service import OmutsuService
_whims_registration_handlers = []

class OmutsuSatisfactionAwardType:
    MONEY = 0
    BUFF = 1
    OBJECT = 2
    TRAIT = 3
    CASPART = 4


class OmutsuSatisfactionService(OmutsuService):

    def register_store_reward(self, sim_reward_id, cost, award_type):
        sim_reward_instance = get_resource_service().get_instance(OmutsuResourceType.REWARD, int(sim_reward_id))
        if sim_reward_instance is not None:
            sim_reward_data_immutable_slots_cls = sims4.collections.make_immutable_slots_class(["cost", "award_type"])
            reward_data = sim_reward_data_immutable_slots_cls(dict(cost=cost, award_type=award_type))
            store_items = dict(SatisfactionTracker.SATISFACTION_STORE_ITEMS)
            store_items[sim_reward_instance] = reward_data
            SatisfactionTracker.SATISFACTION_STORE_ITEMS = sims4.collections.FrozenAttributeDict(store_items)


_SATISFACTION_SERVICE = OmutsuSatisfactionService("satisfaction")

def get_satisfaction_service() -> OmutsuSatisfactionService:
    return _SATISFACTION_SERVICE
