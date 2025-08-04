from protocolbuffers.Localization_pb2 import LocalizedStringToken
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class _OmutsuSimNameMixin(_SuperOmutsuSim):

    @sim_info_required(default=False, base_wrapper=True)
    def has_name(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return sim_info.first_name and sim_info.last_name

    @sim_info_required(default="", base_wrapper=True)
    def get_first_name(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return sim_info.first_name

    @sim_info_required(default="", base_wrapper=True)
    def get_last_name(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return sim_info.last_name

    @sim_info_required(default=('', ''), base_wrapper=True)
    def get_full_name(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return (
         sim_info.first_name, sim_info.last_name)

    @sim_info_required(default=0, base_wrapper=True)
    def get_full_name_key(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return sim_info.full_name_key

    @sim_info_required(base_wrapper=True)
    def populate_localization_token(self, token):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        token.type = LocalizedStringToken.SIM
        token.first_name = sim_info.first_name
        token.last_name = sim_info.last_name
        token.full_name_key = sim_info.full_name_key
        token.is_female = sim_info.is_female
