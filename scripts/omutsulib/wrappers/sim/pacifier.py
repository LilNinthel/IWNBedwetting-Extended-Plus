import random

import iwnbedwetting.main
import sims4.log
from omutsulib.enums.buffs import IwnBedwettingBuff
from omutsulib.enums.pacifiers import AdultPacifiers, ChildPacifiers
from omutsulib.enums.statistics import IwnBedwettingStatistic
from omutsulib.services.cas_service import OmutsuCasPart
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required
from sims.outfits.outfit_enums import BodyType

logger = sims4.log.Logger('IWNBedwettingMain')


class _OmutsuSimPacifierMixin(_SuperOmutsuSim):

    @sim_info_required(default=False)
    def outfit_contains_pacifier(self, outfit_category_and_index=None):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        omutsu_sim = OmutsuSim(self)
        if not omutsu_sim.is_human():
            return False
        if omutsu_sim.is_teen_or_older() or (iwnbedwetting.main._admin_flag and omutsu_sim.is_child()):
            logger.info("Pacifier check on {}".format(self))
            if outfit_category_and_index is None:
                outfit_category_and_index = omutsu_sim.get_current_outfit()
            if outfit_category_and_index is not None:
                outfit_parts = omutsu_sim.get_outfit_parts(outfit_category_and_index)
                if outfit_parts is not None:
                    if BodyType.LIP_RING_LEFT in outfit_parts.keys():
                        for outfit_part in outfit_parts[BodyType.LIP_RING_LEFT]:
                            if omutsu_sim._is_pacifier_cas_part(outfit_part.cas_part):
                                return True
        return False

    @staticmethod
    def _is_pacifier_cas_part(cas_part_id):
        return cas_part_id in AdultPacifiers.get_enum_values() or cas_part_id in ChildPacifiers.get_enum_values()

    @sim_info_required()
    def suck_favorite_pacifier(self):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        omutsu_sim = OmutsuSim(self)
        if not omutsu_sim.is_human():
            return
        logger.info("iwn.suck_favorite_pacifier: {}", self)
        paci_index = omutsu_sim.get_statistic_value(IwnBedwettingStatistic.FAVORITE_PACIFIER)
        if paci_index is None or paci_index < 0:
            omutsu_sim.suck_random_pacifier()
        else:
            paci_index = int(paci_index)
            outfit_category_and_index = omutsu_sim.get_current_outfit()
            if outfit_category_and_index is not None:
                outfit_parts = omutsu_sim.get_outfit_parts(outfit_category_and_index)
                if outfit_parts is not None:
                    pacifiers = list()
                    if omutsu_sim.is_teen_or_older():
                        pacifiers = AdultPacifiers.get_enum_values_ordered()
                    elif iwnbedwetting.main._admin_flag and omutsu_sim.is_child():
                        pacifiers = ChildPacifiers.get_enum_values_ordered()
                    if paci_index < len(pacifiers):
                        outfit_parts[BodyType.LIP_RING_LEFT] = (OmutsuCasPart((pacifiers[paci_index])),)
                        omutsu_sim.set_outfit_parts(outfit_category_and_index, outfit_parts)
                        omutsu_sim.set_statistic_value(IwnBedwettingStatistic.CURRENT_PACIFIER, paci_index)
                        omutsu_sim.add_buff(IwnBedwettingBuff.HAS_PACIFIER)
                    else:
                        omutsu_sim.remove_statistic(IwnBedwettingStatistic.FAVORITE_PACIFIER)

    @sim_info_required()
    def suck_random_pacifier(self):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        omutsu_sim = OmutsuSim(self)
        if not omutsu_sim.is_human():
            return
        logger.info("iwn.suck_random_pacifier: {}", self)
        outfit_category_and_index = omutsu_sim.get_current_outfit()
        logger.info("iwn.suck_random_pacifier outfit: {}", outfit_category_and_index)
        if outfit_category_and_index is not None:
            outfit_parts = omutsu_sim.get_outfit_parts(outfit_category_and_index)
            # logger.info("iwn.suck_random_pacifier outfit_parts: {}", outfit_parts)
            if outfit_parts is not None:
                # if BodyType.LIP_RING_LEFT in outfit_parts.keys():
                #     for outfit_part in outfit_parts[BodyType.LIP_RING_LEFT]:
                #         if is_pacifier(outfit_part.cas_part):
                #             return
                paci_cas_id = 0
                if omutsu_sim.is_teen_or_older():
                    paci_cas_id = random.choice(AdultPacifiers.get_enum_values_ordered())
                elif iwnbedwetting.main._admin_flag and omutsu_sim.is_child():
                    paci_cas_id = random.choice(ChildPacifiers.get_enum_values_ordered())
                if paci_cas_id != 0:
                    logger.info("Pacifier CAS part: {}", paci_cas_id)
                    outfit_parts[BodyType.LIP_RING_LEFT] = (OmutsuCasPart((paci_cas_id)),)
                    omutsu_sim.set_outfit_parts(outfit_category_and_index, outfit_parts)
                    paci_index = self.get_pacifier_index(omutsu_sim, OmutsuCasPart((paci_cas_id)))
                    omutsu_sim.set_statistic_value(IwnBedwettingStatistic.CURRENT_PACIFIER, paci_index)
                    omutsu_sim.add_buff(IwnBedwettingBuff.HAS_PACIFIER)

    @sim_info_required()
    def remove_pacifier(self):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        omutsu_sim = OmutsuSim(self)
        if not omutsu_sim.is_human():
            return
        logger.info("iwn.remove_pacifier: {}", self)
        outfit_category_and_index = omutsu_sim.get_current_outfit()
        if outfit_category_and_index is not None:
            outfit_parts = omutsu_sim.get_outfit_parts(outfit_category_and_index)
            if outfit_parts is not None:
                if BodyType.LIP_RING_LEFT in outfit_parts.keys():
                    for outfit_part in outfit_parts[BodyType.LIP_RING_LEFT]:
                        if omutsu_sim._is_pacifier_cas_part(outfit_part.cas_part):
                            outfit_parts.pop(BodyType.LIP_RING_LEFT)
                    omutsu_sim.set_outfit_parts(outfit_category_and_index, outfit_parts)
                    omutsu_sim.remove_statistic(IwnBedwettingStatistic.CURRENT_PACIFIER)
                    omutsu_sim.remove_buff(IwnBedwettingBuff.HAS_PACIFIER)

    @sim_info_required()
    def set_favorite_pacifier(self):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        omutsu_sim = OmutsuSim(self)
        if not omutsu_sim.is_human():
            return
        logger.info("iwn.set_favorite_pacifier: {}", self)
        outfit_category_and_index = omutsu_sim.get_current_outfit()
        if outfit_category_and_index is not None:
            outfit_parts = omutsu_sim.get_outfit_parts(outfit_category_and_index)
            if outfit_parts is not None:
                if BodyType.LIP_RING_LEFT in outfit_parts.keys():
                    for outfit_part in outfit_parts[BodyType.LIP_RING_LEFT]:
                        if omutsu_sim._is_pacifier_cas_part(outfit_part.cas_part):
                            paci_index = self.get_pacifier_index(omutsu_sim, outfit_part)
                            omutsu_sim.set_statistic_value(IwnBedwettingStatistic.FAVORITE_PACIFIER, paci_index)

    @staticmethod
    def get_pacifier_index(omutsu_sim, outfit_part):
        if iwnbedwetting.main._admin_flag and omutsu_sim.is_child():
            paci_index = ChildPacifiers.get_enum_values_ordered().index(outfit_part.cas_part)
        else:
            paci_index = AdultPacifiers.get_enum_values_ordered().index(outfit_part.cas_part)
        return paci_index

