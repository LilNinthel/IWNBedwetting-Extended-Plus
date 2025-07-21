import traceback

import services
import sims4.log
from iwnbedwetting.enums.tunable import DiaperWetness, DiaperMessiness
from sims.outfits.outfit_enums import BodyType
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import HasTunableReferenceFactory, Tunable, TunableTuple, TunableList, TunableEnumEntry, TunableCasPart

logger = sims4.log.Logger('DiaperLoadCASConfig')


class DiaperLoadCASConfig(HasTunableReferenceFactory, metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(Types.SNIPPET)):

    supported_cc_installed = False

    _default_diaper_lookup = dict()

    _default_diaper_lookup_by_part = dict()

    _diaper_config = dict()

    INSTANCE_TUNABLES = {
        'diaper_cc_list': TunableList(
            description='A list of CAS diaper CC and the configuration for mapping wetness/messiness to different swatches',
            tunable=TunableTuple(
                body_type=TunableEnumEntry(description="The BodyType for this CAS part", tunable_type=BodyType, default=None),
                default_cas_part=TunableCasPart(description="""
                The CAS part that represents the default dry/clean state for the diaper
                """),
                diaper_load_config=TunableList(
                    description='A list of consumable interactions to add to the objects',
                    tunable=TunableTuple(
                        description='Reference to an interaction tuning instance',
                        wetness_level=Tunable(description="Diaper wetness", tunable_type=int, default=0),
                        mess_level=Tunable(description="Diaper messiness", tunable_type=int, default=0),
                        cas_part=TunableCasPart(description="""
                                        The CAS part that represents this state for the diaper
                                        """)
                        ),
                    allow_none=False
                )
            ),
            allow_none=False,
            unique_entries=True
        )
    }

    @staticmethod
    def get_default_cas_part(diaper_cas_part_id):
        if DiaperLoadCASConfig.supported_cc_installed:
            if diaper_cas_part_id in DiaperLoadCASConfig._default_diaper_lookup.keys():
                return DiaperLoadCASConfig._default_diaper_lookup[diaper_cas_part_id]
        return None

    @staticmethod
    def get_diaper_cas_part_ids():
        return DiaperLoadCASConfig._default_diaper_lookup.keys()

    @staticmethod
    def get_default_diaper_parts_ids_for_body_type(body_type, filter = None):
        if body_type in DiaperLoadCASConfig._default_diaper_lookup_by_part.keys():
            diapers = DiaperLoadCASConfig._default_diaper_lookup_by_part[body_type]
            if filter is not None:
                diapers = [x for x in diapers if x in filter]
            return diapers
        return list()

    _hardcoded_diaper_parts = frozenset({17916267921504688060,16089036029714611952})

    @staticmethod
    def is_diaper_part(cas_part_id):
        return cas_part_id in DiaperLoadCASConfig._default_diaper_lookup.keys() or cas_part_id in DiaperLoadCASConfig._hardcoded_diaper_parts

    @staticmethod
    def get_diaper_config(cas_part_id):
        if DiaperLoadCASConfig.is_diaper_part(cas_part_id) and cas_part_id in DiaperLoadCASConfig._default_diaper_lookup.keys() and DiaperLoadCASConfig._default_diaper_lookup[cas_part_id] in DiaperLoadCASConfig._diaper_config.keys():
            return DiaperLoadCASConfig._diaper_config[DiaperLoadCASConfig._default_diaper_lookup[cas_part_id]]
        return None

    @classmethod
    def _tuning_loaded_callback(cls) -> None:
        logger.info('Processing {}', str(cls))
        try:
            for diaper_cc in cls.diaper_cc_list:
                configured_states = dict()
                if diaper_cc.body_type is None:
                    continue
                if diaper_cc.default_cas_part is None:
                    continue
                logger.info("diaper_cc: {}".format(diaper_cc))
                logger.info("body_type: {}".format(diaper_cc.body_type))
                logger.info("default_cas_part: {}".format(diaper_cc.default_cas_part))
                DiaperLoadCASConfig._default_diaper_lookup[diaper_cc.default_cas_part] = diaper_cc.default_cas_part
                if diaper_cc.body_type not in DiaperLoadCASConfig._default_diaper_lookup_by_part.keys():
                    DiaperLoadCASConfig._default_diaper_lookup_by_part[diaper_cc.body_type] = list()
                if diaper_cc.default_cas_part not in DiaperLoadCASConfig._default_diaper_lookup_by_part[diaper_cc.body_type]:
                    DiaperLoadCASConfig._default_diaper_lookup_by_part[diaper_cc.body_type].append(diaper_cc.default_cas_part)
                DiaperLoadCASConfig._diaper_config[diaper_cc.default_cas_part] = diaper_cc
                for diaperState in diaper_cc.diaper_load_config:
                    logger.info(' diaperState : {}', diaperState)
                    if diaperState.wetness_level == DiaperWetness.DRY and diaperState.mess_level == DiaperMessiness.CLEAN:
                        logger.warn(' Dry and clean diaper cannot be configured here, ignoring entry')
                        continue
                    stateKey = (diaperState.wetness_level,diaperState.mess_level)
                    if stateKey in configured_states.keys():
                        logger.warn(' Duplicate state config for {}, ignoring entry', stateKey)
                        continue

                    if diaperState.cas_part is None:
                        logger.warn(' Failed to find CAS entry')
                        continue

                    configured_states[stateKey] = diaperState
                    DiaperLoadCASConfig._default_diaper_lookup[diaperState.cas_part] = diaper_cc.default_cas_part

            DiaperLoadCASConfig.supported_cc_installed = True
        except:
            logger.error('Exception occurred processing DiaperLoadCASConfig tuning instance {}', str(cls))
            logger.error(traceback.format_exc())

    def __repr__(self):
        return '<DiaperLoadCASConfig:({})>'.format(self.__name__)

    def __str__(self):
        return '{}'.format(self.__name__)
