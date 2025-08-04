from omutsulib.wrappers.enum import OmutsuIntFlagsEnum, OmutsuIntEnum
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class OmutsuAge(OmutsuIntFlagsEnum):
    NONE = 0
    BABY = 1
    TODDLER = 2
    CHILD = 4
    TEEN = 8
    YOUNGADULT = 16
    ADULT = 32
    ELDER = 64
    INFANT = 128
    AGE_ORDER_INDEX = dict(((age, index) for (index, age) in enumerate((NONE, BABY, INFANT, TODDLER, CHILD, TEEN, YOUNGADULT, ADULT, ELDER))))

    def __lt__(self, age):
        return self.AGE_ORDER_INDEX[self] < self.AGE_ORDER_INDEX[age]

    def __le__(self, age):
        return self.AGE_ORDER_INDEX[self] <= self.AGE_ORDER_INDEX[age]

    def __gt__(self, age):
        return self.AGE_ORDER_INDEX[self] > self.AGE_ORDER_INDEX[age]

    def __ge__(self, age):
        return self.AGE_ORDER_INDEX[self] >= self.AGE_ORDER_INDEX[age]

    def get_order(self):
        return self.AGE_ORDER_INDEX[self]


class OmutsuAgeSpeed(OmutsuIntEnum):
    FAST = 0
    NORMAL = 1
    SLOW = 2


class _OmutsuSimAgeMixin(_SuperOmutsuSim):

    @sim_info_required(default=(OmutsuAge(0)), base_wrapper=True)
    def get_age(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return OmutsuAge(sim_info._base.age or 0)

    @sim_info_required(default=False, base_wrapper=True)
    def is_child(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return OmutsuAge(sim_info._base.age or 0) == OmutsuAge.CHILD

    @sim_info_required(default=False, base_wrapper=True)
    def is_teen_or_older(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return OmutsuAge(sim_info._base.age or 0) >= OmutsuAge.TEEN

    @sim_info_required(base_wrapper=True)
    def set_age(self, age):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info.apply_age(age)

    @sim_info_required(default=0, base_wrapper=True)
    def get_age_duration(self, age=None):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        age_transition_data = sim_info.get_age_transition_data(age or self.get_age())
        age_duration = age_transition_data.get_age_duration(sim_info)
        return age_duration
