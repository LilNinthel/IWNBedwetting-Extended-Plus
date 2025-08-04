import weakref, services
from objects import ALL_HIDDEN_REASONS_EXCEPT_UNINITIALIZED, ALL_HIDDEN_REASONS
from sims.household import Household
from omutsulib.services.persistence_service import get_persistence_service
from omutsulib.services.world_service import get_zone_service
from omutsulib.utils.singletons import EMPTY_DICT
from omutsulib.wrappers.wrappers_manager import OmutsuInstance, OmutsuInstanceSingleton
_super_household_persistence_key_cache = None

def _update_persistence_key(from_load=False, **_):
    global _super_household_persistence_key_cache
    if from_load:
        _super_household_persistence_key_cache = OmutsuHouseholdSingleton.create_persistence_key()


get_persistence_service().register_save_slot_id_update_callback(_update_persistence_key)

class OmutsuFundsType:
    INTERACTION_COST = 1
    INTERACTION_REWARD = 2
    EVENT_COST = 3
    EVENET_REWARD = 4
    OBJECT_BUY = 5
    OBJECT_SELL = 6
    STRUCTURE_BUY = 7
    STRUCTURE_SELL = 8
    CAS_BUY = 9
    BLUEPRINT_CONSTRUCTED = 10
    LOT_BUY = 11
    LOT_SELL = 12
    HOUSEHOLD_TRANSFER_GAIN = 13
    HOUSEHOLD_TRANSFER_LOSS = 14
    SIM_POINTS_EXCHANGED = 15
    SIM_WALLET_FUNDED = 16
    SIM_WALLET_EMPTIED = 17
    CRAFTING_COST = 18
    MONEY_CHEAT = 19
    MONEY_CAREER = 20
    MONEY_ASPIRATION_REWARD = 21
    MONEY_ROYALTY = 22
    MONEY_FIREINSURANCE = 23
    MONEY_VACATION = 24
    RETAIL_ITEM_BUY = 25
    RETAIL_PROFITS = 26
    RETAIL_TRANSFER_GAIN = 27
    RETAIL_TRANSFER_LOSS = 28
    HOLIDAY_LOTTERY = 29
    LIFESTYLE_BRAND = 30
    ROOMMATE_RENT = 31
    SPLIT_HOUSEHOLD = 32
    TUITION_COST = 33
    SCHOLARSHIP_SURPLUS = 34
    SMALL_BUSINESS_INTERACTION_REWARD = 35
    SMALL_BUSINESS_HOURLY_FEE_REWARD = 36
    SMALL_BUSINESS_ENTRY_FEE_REWARD = 37
    SMALL_BUSINESS_LIGHT_RETAIL_REWARD = 38
    SMALL_BUSINESS_SELL_BUSINESS_VALUE = 39
    SMALL_BUSINESS_OPEN_BUSINESS = 40
    SMALL_BUSINESS_EMPLOYEE = 41


class OmutsuAdditionalBillSource:
    Miscellaneous = 0
    MaidService = 1
    PizzaDelivery = 2
    RepairService = 3
    GardeningService = 4
    NannyService = 5
    ButlerService = 6
    RanchHandService = 7
    TaxesPerRentalUnit = 8


class OmutsuHouseholdSingleton(OmutsuInstanceSingleton):
    _is_persistent = True

    def get_key(cls, object_instance, *args, **kwargs):
        household_id = _get_household_instance_id(object_instance)
        if household_id is not None:
            return (household_id, cls.__name__)

    @staticmethod
    def create_persistence_key():
        return (
         get_persistence_service().get_save_slot_guid(), get_persistence_service().get_save_slot_id())

    def get_persistence_key(cls):
        global _super_household_persistence_key_cache
        if _super_household_persistence_key_cache is None:
            _super_household_persistence_key_cache = cls.create_persistence_key()
        return _super_household_persistence_key_cache


class _SuperOmutsuHousehold(OmutsuInstance):

    def __init__(self, *args):
        household_identifier = args[0]
        self._household_id = _get_household_instance_id(household_identifier)
        self._household_instance = None
        super().__init__(self._household_id)

    def __new__(cls, *args):
        household_identifier = args[0]
        if isinstance(household_identifier, _SuperOmutsuHousehold):
            return household_identifier
        if _get_household_instance_id(household_identifier) is None:
            return
        return super().__new__(cls)

    def get_id(self):
        return self._household_id

    def get_household_instance(self):
        if self._household_instance is not None:
            household_instance = self._household_instance()
            if household_instance is not None:
                return household_instance
            household_instance = services.household_manager().get(self._household_id)
            if household_instance is None:
                return
            self._household_instance = weakref.ref(household_instance)
            return household_instance

    def set_creator_data(self, creator_id, creator_name, creator_uuid):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            household_instance.creator_id = creator_id
            household_instance.creator_name = creator_name
            household_instance.creator_uuid = creator_uuid

    def remove(self):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            services.household_manager().remove(household_instance)
            return True
        return False

    def get_name(self):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            return household_instance.name
        return ""

    def set_name(self, name):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            household_instance.name = name

    def get_description(self):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            return household_instance.description
        return ""

    def set_description(self, description):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            household_instance.description = description

    def get_zone_id(self):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            return household_instance.home_zone_id
        return 0

    def is_played(self):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            return household_instance.is_player_household
        return False

    def get_size(self):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            return household_instance.household_size
        return 0

    def get_omutsu_sims_gen(self, instanced=False, age=None, species=None, valid=True):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        household_instance = self.get_household_instance()
        if household_instance is not None:
            for sim_info in household_instance.sim_info_gen():
                if sim_info is not None:
                    if species:
                        if species != sim_info.species:
                            continue
                        if age:
                            if not age & sim_info.age:
                                continue
                            if instanced:
                                sim_instance = sim_info.get_sim_instance(allow_hidden_flags=(ALL_HIDDEN_REASONS_EXCEPT_UNINITIALIZED if valid else ALL_HIDDEN_REASONS))
                                if sim_instance is not None:
                                    yield OmutsuSim(sim_instance)
                            else:
                                yield OmutsuSim(sim_info)

    def get_free_sims_slots(self):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            return household_instance.free_slot_count
        return 0

    def get_funds(self):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            return household_instance.funds.money
        return 0

    def add_funds(self, amount, funds_type=OmutsuFundsType.MONEY_CHEAT, **kwargs):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            (household_instance.funds.add)((max(0, int(amount))), funds_type, **kwargs)

    def subtract_funds(self, amount, funds_type=OmutsuFundsType.MONEY_CHEAT, **kwargs):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            return (household_instance.funds.try_remove)((max(0, int(amount))), funds_type, **kwargs)

    def add_additional_bill_cost(self, amount, additional_bill_source=OmutsuAdditionalBillSource.Miscellaneous):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            household_instance.bills_manager.add_additional_bill_cost(additional_bill_source, amount)

    def owns_business_type(self, business_type):
        business_service = services.business_service()
        if business_service is not None:
            business_managers = business_service.get_business_managers_for_household()
            if business_managers:
                business_manager = business_managers.get(get_zone_service().get_current_zone_id(), None)
                if business_manager is not None:
                    if business_manager.business_type == business_type:
                        return False
                    if any((business_manager.business_type == business_type for business_manager in business_managers.values())):
                        return True
            return False

    def is_story_progression_enabled(self):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            if household_instance.story_progression_rule_set is not None:
                return household_instance.story_progression_rule_set.enabled
            return False

    def get_story_progression_rules(self):
        household_instance = self.get_household_instance()
        if household_instance is not None and household_instance.story_progression_rule_set is not None:
            if household_instance.story_progression_rule_set._rules:
                return household_instance.story_progression_rule_set._rules
            if household_instance.story_progression_rule_set._parent_rule_set is not None:
                return household_instance.story_progression_rule_set._parent_rule_set._rules
            return EMPTY_DICT

    def set_story_progression_rule(self, rule_id, state):
        household_instance = self.get_household_instance()
        if household_instance is not None:
            if household_instance.story_progression_rule_set is not None:
                household_instance.story_progression_rule_set._rules[rule_id] = state


class OmutsuHousehold(_SuperOmutsuHousehold, metaclass=OmutsuHouseholdSingleton):

    def __init__(self, *args):
        household_identifier = args[0]
        super().__init__(household_identifier)


def _get_household_instance_id(household_identifier):
    if household_identifier is None:
        return
    if isinstance(household_identifier, Household):
        return getattr(household_identifier, "id", None)
    if isinstance(household_identifier, int):
        return household_identifier
    if isinstance(household_identifier, _SuperOmutsuHousehold):
        return household_identifier.get_instance_id()
