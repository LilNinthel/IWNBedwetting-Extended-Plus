import collections, inspect, itertools, sys
from interactions.utils.tunable_provided_affordances import TunableProvidedAffordances
from objects.game_object import GameObject
from services.terrain_service import TerrainService
from sims4.tuning.instance_manager import InstanceManager
from omutsulib.services.components_service import get_components_service, OmutsuComponentType
from omutsulib.services.resources_service import OmutsuResourceType, get_resource_service
from omutsulib.services.service import OmutsuService
from omutsulib.utils.injector import inject
from omutsulib.utils.tunables import create_tunable_instance
from omutsulib.utils.types import is_sim_instance
from omutsulib.wrappers.enum import OmutsuIntFlagsEnum
from omutsulib.wrappers.game_object.game_object import OmutsuGameObject
from omutsulib.wrappers.logger import OmutsuLogger
from omutsulib.wrappers.sim.sim import OmutsuSim
logger = OmutsuLogger("AffordanceInjection")
AFFORDANCE_LIST_CLASS = getattr(sys.modules.get("snippets", None), "AffordanceList", None)

class AffordanceTargetType(OmutsuIntFlagsEnum):
    OBJECT = 1
    PHONE = 2
    RELATIONSHIP_PANEL = 4
    TERRAIN = 8
    WATER = 16
    MIXER = 32
    SOCIAL_MIXER = 64
    BUFF = 128
    TRAIT = 256
    AUTO_CONSTRAINTS_TRANSFER = 512
    ALL_OBJECTS = OBJECT | PHONE | RELATIONSHIP_PANEL
    ALL_ENVIRONMENT = TERRAIN | WATER


class AffordanceProviderDestinationType(OmutsuIntFlagsEnum):
    SI_ACTOR = 1
    SI_TARGET = 2


class AffordanceFlagType(OmutsuIntFlagsEnum):
    NONE = 0
    STATIC = 1
    LOCKING = 2


class OmutsuAffordancesService(OmutsuService):

    def __init__(self, name):
        super().__init__(name)
        self.affordance_registration_handlers = collections.defaultdict(list)

    def register_affordances_handler(self, affordances_handler, **kwargs):
        affordances_handler_instance = affordances_handler(**kwargs)
        for target_type in AffordanceTargetType:
            if target_type & affordances_handler_instance.target:
                self.affordance_registration_handlers[target_type].append(affordances_handler_instance)
                logger.info("Registered {} Affordance Handler.".format(affordances_handler.__name__))

    def get_affordances_handlers(self, target_type):
        return self.affordance_registration_handlers[target_type]

    def add_object_affordances(self, script_object):
        if is_sim_instance(script_object):
            omutsu_object = OmutsuSim(script_object)
        else:
            omutsu_object = OmutsuGameObject(script_object)
        if omutsu_object is not None:
            for affordances_handler in self.get_affordances_handlers(AffordanceTargetType.OBJECT):
                if not affordances_handler.has_expired:
                    if affordances_handler.test(omutsu_object):
                        if AffordanceFlagType.LOCKING & affordances_handler.flags and get_components_service().has_object_component(script_object, OmutsuComponentType.OBJECT_LOCKING):
                            object_locking_component = get_components_service().get_object_component(script_object, OmutsuComponentType.OBJECT_LOCKING)
                            if object_locking_component is not None:
                                try:
                                    object_locked_affordance_instances = {affordance_instance for affordance_instance in affordances_handler._get_affordance_instances() if affordance_instance not in object_locking_component.super_affordances}
                                    if object_locked_affordance_instances:
                                        object_locking_component.super_affordances |= object_locked_affordance_instances
                                        logger.info("Added object locking affordances to {}:\n{}".format(script_object.__class__.__name__, "\n".join([next(iter(affordance_instance.get_parents()), None).__name__ for affordance_instance in object_locked_affordance_instances])))
                                except Exception as ex:
                                    try:
                                        pass  # log_custom_exception("[OmutsuLib] Failed to run 'add_object_affordances' for {} Locking Object Affordance Handler.".format(affordances_handler.__class__.__name__), ex)
                                    finally:
                                        ex = None
                                        del ex

                        else:
                            try:
                                object_affordance_instances = [affordance_instance for affordance_instance in affordances_handler._get_affordance_instances() if affordance_instance not in script_object._super_affordances]
                                if object_affordance_instances:
                                    script_object._super_affordances += tuple(object_affordance_instances)
                                    logger.info("Added object affordances to {}:\n{}".format(script_object.__class__.__name__, "\n".join([next(iter(affordance_instance.get_parents()), None).__name__ for affordance_instance in object_affordance_instances])))
                            except Exception as ex:
                                try:
                                    pass  # log_custom_exception("[OmutsuLib] Failed to run 'add_object_affordances' for {} Object Affordance Handler.".format(affordances_handler.__class__.__name__), ex)
                                finally:
                                    ex = None
                                    del ex

                        if AffordanceFlagType.STATIC & affordances_handler.flags:
                            object_class_affordance_instances = [affordance_instance for affordance_instance in affordances_handler._get_affordance_instances() if affordance_instance not in script_object.__class__._super_affordances]
                            if object_class_affordance_instances:
                                script_object.__class__._super_affordances += tuple(object_class_affordance_instances)
                                script_object.clear_commodity_flags()
                                logger.info("Added static object affordances to {}:\n{}".format(script_object.__class__.__name__, "\n".join([next(iter(affordance_instance.get_parents()), None).__name__ for affordance_instance in object_class_affordance_instances])))

            if isinstance(omutsu_object, OmutsuSim):
                for affordances_handler in self.get_affordances_handlers(AffordanceTargetType.PHONE):
                    if not affordances_handler.has_expired:
                        if affordances_handler.test(omutsu_object):
                            try:
                                phone_affordance_instances = [affordance_instance for affordance_instance in affordances_handler._get_affordance_instances() if affordance_instance not in script_object._phone_affordances]
                                if phone_affordance_instances:
                                    script_object.__class__._phone_affordances += tuple(phone_affordance_instances)
                                    script_object.clear_commodity_flags()
                                    logger.info("Added phone affordances to {}:\n{}".format(script_object.__class__.__name__, "\n".join([next(iter(affordance_instance.get_parents()), None).__name__ for affordance_instance in phone_affordance_instances])))
                            except Exception as ex:
                                try:
                                    pass  # log_custom_exception("[OmutsuLib] Failed to run 'add_object_affordances' for {} Phone Affordance Handler.".format(affordances_handler.__class__.__name__), ex)
                                finally:
                                    ex = None
                                    del ex

                for affordances_handler in self.get_affordances_handlers(AffordanceTargetType.RELATIONSHIP_PANEL):
                    if not affordances_handler.has_expired:
                        if affordances_handler.test(omutsu_object):
                            try:
                                relationship_panel_affordance_instances = [affordance_instance for affordance_instance in affordances_handler._get_affordance_instances() if affordance_instance not in script_object._relation_panel_affordances]
                                if relationship_panel_affordance_instances:
                                    script_object.__class__._relation_panel_affordances += tuple(relationship_panel_affordance_instances)
                                    script_object.clear_commodity_flags()
                                    logger.info("Added relationship affordances to {}:\n{}".format(script_object.__class__.__name__, "\n".join([next(iter(affordance_instance.get_parents()), None).__name__ for affordance_instance in relationship_panel_affordance_instances])))
                            except Exception as ex:
                                try:
                                    pass  # log_custom_exception("[OmutsuLib] Failed to run 'add_object_affordances' for {} Relationship Panel Affordance Handler.".format(affordances_handler.__class__.__name__), ex)
                                finally:
                                    ex = None
                                    del ex

    def add_environment_affordances(self, definition_cls, target=AffordanceTargetType.ALL_ENVIRONMENT):
        environment_affordance_instances = set()
        for affordances_handler in itertools.chain(self.get_affordances_handlers(AffordanceTargetType.TERRAIN), self.get_affordances_handlers(AffordanceTargetType.WATER)):
            if not affordances_handler.has_expired:
                if target & affordances_handler.target:
                    try:
                        environment_affordance_instances.update([affordance_instance for affordance_instance in affordances_handler._get_affordance_instances() if affordance_instance not in definition_cls._super_affordances])
                    except Exception as ex:
                        try:
                            pass  # log_custom_exception("[OmutsuLib] Failed to run 'add_environment_affordances' for {} Environment Affordance Handler.".format(affordances_handler.__class__.__name__), ex)
                        finally:
                            ex = None
                            del ex

        if environment_affordance_instances:
            definition_cls._super_affordances += tuple(environment_affordance_instances)
            if AffordanceTargetType.TERRAIN & target:
                TerrainService.TERRAIN_DEFINITION.set_class(definition_cls)
            if AffordanceTargetType.WATER & target:
                TerrainService.OCEAN_DEFINITION.set_class(definition_cls)
            logger.info("Added environment affordances:\n{}".format("\n".join([next(iter(affordance_instance.get_parents()), None).__name__ for affordance_instance in environment_affordance_instances])))

    def add_mixer_affordances(self, affordance_snippets):
        for affordances_handler in itertools.chain(self.get_affordances_handlers(AffordanceTargetType.MIXER), self.get_affordances_handlers(AffordanceTargetType.SOCIAL_MIXER)):
            if not affordances_handler.has_expired:
                mixer_affordance_instances = None
                for affordance_list_id in affordances_handler.get_affordance_lists():
                    if affordance_list_id in affordance_snippets:
                        affordance_list_instance = affordance_snippets[affordance_list_id]
                        if mixer_affordance_instances is None:
                            try:
                                mixer_affordance_instances = [affordance_instance for affordance_instance in affordances_handler._get_affordance_instances() if affordance_instance not in affordance_list_instance.value]
                            except Exception as ex:
                                try:
                                    pass  # log_custom_exception("[OmutsuLib] Failed to run 'add_mixer_affordances' for {} Mixer Affordance Handler.".format(affordances_handler.__class__.__name__), ex)
                                finally:
                                    ex = None
                                    del ex

                            if mixer_affordance_instances:
                                affordance_list_instance.value += tuple(mixer_affordance_instances)
                                logger.info("Added mixer affordances to {}:\n{}".format(next(iter(affordance_list_instance.get_parents()), None).__name__, "\n".join([next(iter(affordance_instance.get_parents()), None).__name__ for affordance_instance in mixer_affordance_instances])))

    def add_buff_affordances(self, buff_instances):
        for affordances_handler in self.get_affordances_handlers(AffordanceTargetType.BUFF):
            if not affordances_handler.has_expired:
                buff_affordance_instances = None
                for buff_id in affordances_handler.get_buffs():
                    if buff_id in buff_instances:
                        buff_instance = buff_instances[buff_id]
                        buff_instance_affordances = set()
                        if AffordanceProviderDestinationType.SI_ACTOR & affordances_handler.destination:
                            buff_instance_affordances.update(buff_instance.super_affordances)
                        if AffordanceProviderDestinationType.SI_TARGET & affordances_handler.destination:
                            buff_instance_affordances.update((provided_affordance_data.affordance for provided_affordance_data in buff_instance.target_super_affordances))
                        if buff_affordance_instances is None:
                            try:
                                buff_affordance_instances = [affordance_instance for affordance_instance in affordances_handler._get_affordance_instances() if affordance_instance not in buff_instance_affordances]
                            except Exception as ex:
                                try:
                                    pass  # log_custom_exception("[OmutsuLib] Failed to run 'add_buff_affordances' for {} Buff Affordance Handler.".format(affordances_handler.__class__.__name__), ex)
                                finally:
                                    ex = None
                                    del ex

                            if buff_affordance_instances:
                                if AffordanceProviderDestinationType.SI_ACTOR & affordances_handler.destination:
                                    buff_instance.super_affordances = set(buff_instance.super_affordances) | set(buff_affordance_instances)
                                if AffordanceProviderDestinationType.SI_TARGET & affordances_handler.destination:
                                    buff_instance.target_super_affordances = list(buff_instance.target_super_affordances) + [create_tunable_instance(TunableProvidedAffordances, affordance=affordance) for affordance in buff_affordance_instances]
                                logger.info("Added buff affordances to {}:\n{}".format(next(iter(buff_instance.get_parents()), None).__name__, "\n".join([next(iter(affordance_instance.get_parents()), None).__name__ for affordance_instance in buff_affordance_instances])))

                affordances_handler.expire()

    def add_trait_affordances(self, trait_instances):
        for affordances_handler in self.get_affordances_handlers(AffordanceTargetType.TRAIT):
            if not affordances_handler.has_expired:
                trait_affordance_instances = None
                for trait_id in affordances_handler.get_traits():
                    if trait_id in trait_instances:
                        trait_instance = trait_instances[trait_id]
                        trait_instance_affordances = set()
                        if AffordanceProviderDestinationType.SI_ACTOR & affordances_handler.destination:
                            trait_instance_affordances.update(trait_instance.super_affordances)
                        if AffordanceProviderDestinationType.SI_TARGET & affordances_handler.destination:
                            trait_instance_affordances.update((provided_affordance_data.affordance for provided_affordance_data in trait_instance.target_super_affordances))
                        if trait_affordance_instances is None:
                            try:
                                trait_affordance_instances = [affordance_instance for affordance_instance in affordances_handler._get_affordance_instances() if affordance_instance not in trait_instance_affordances]
                            except Exception as ex:
                                try:
                                    pass  # log_custom_exception("[OmutsuLib] Failed to run 'add_trait_affordances' for {} Trait Affordance Handler.".format(affordances_handler.__class__.__name__), ex)
                                finally:
                                    ex = None
                                    del ex

                            if trait_affordance_instances:
                                if AffordanceProviderDestinationType.SI_ACTOR & affordances_handler.destination:
                                    trait_instance.super_affordances = set(trait_instance.super_affordances) | set(trait_affordance_instances)
                                if AffordanceProviderDestinationType.SI_TARGET & affordances_handler.destination:
                                    trait_instance.target_super_affordances = list(trait_instance.target_super_affordances) + [create_tunable_instance(TunableProvidedAffordances, affordance=affordance) for affordance in trait_affordance_instances]
                                logger.info("Added trait affordances to {}:\n{}".format(next(iter(trait_instance.get_parents()), None).__name__, "\n".join([next(iter(affordance_instance.get_parents()), None).__name__ for affordance_instance in trait_affordance_instances])))

                affordances_handler.expire()

    def add_miscellaneous_affordances(self):
        for affordances_handler in self.get_affordances_handlers(AffordanceTargetType.AUTO_CONSTRAINTS_TRANSFER):
            if not affordances_handler.has_expired:
                affordance_manager = get_resource_service().get_instance_manager(OmutsuResourceType.INTERACTION)
                ac_pairs = affordances_handler.get_ac_transfer_pairs()
                for affordance_instance in affordances_handler._get_affordance_instances():
                    ac_source_affordance_id = ac_pairs[affordance_instance.guid64]
                    ac_source_affordance = get_resource_service().get_instance_from_manager(affordance_manager, ac_source_affordance_id)
                    if ac_source_affordance is not None:
                        ac_constraints = ac_source_affordance._auto_constraints
                        if ac_constraints is not None:
                            affordance_instance._auto_constraints = ac_constraints
                            logger.info("Added Auto Constraint to affordance:\n{}".format(next(iter(affordance_instance.get_parents()), None).__name__))

                affordances_handler.expire()


_AFFORDANCES_SERVICE = OmutsuAffordancesService("affordances")

def get_affordances_service() -> OmutsuAffordancesService:
    return _AFFORDANCES_SERVICE


def register_affordance_handler():

    def _wrapper(affordance_class):
        get_affordances_service().register_affordances_handler(affordance_class)
        return affordance_class

    return _wrapper


class _AffordanceRegistrationBase:

    def __init__(self, target, flags=AffordanceFlagType.NONE):
        self.target = target
        self.flags = flags
        self._affordances = None
        self.has_expired = False

    def get_affordances(self):
        raise NotImplementedError

    def expire(self):
        self.has_expired = True
        self._affordances = None

    def _get_affordance_instances(self):
        if self._affordances is None:
            self._affordances = [affordance_instance for affordance_instance in self._cache_affordance_instances_gen()]
        return self._affordances

    def _cache_affordance_instances_gen(self):
        affordance_manager = get_resource_service().get_instance_manager(OmutsuResourceType.INTERACTION)
        for affordance_id in self.get_affordances():
            affordance_instance = get_resource_service().get_instance_from_manager(affordance_manager, affordance_id)
            if affordance_instance is not None:
                yield affordance_instance


class ObjectAffordanceRegistration(_AffordanceRegistrationBase):

    def __init__(self, target=AffordanceTargetType.OBJECT, flags=AffordanceFlagType.NONE):
        super().__init__(target, flags=flags)

    def get_affordances(self):
        raise NotImplementedError

    def test(self, omutsu_game_object: OmutsuGameObject):
        raise NotImplementedError


class AutoConstraintTransferAffordanceRegistration(_AffordanceRegistrationBase):

    def __init__(self, target=AffordanceTargetType.AUTO_CONSTRAINTS_TRANSFER, flags=AffordanceFlagType.NONE):
        super().__init__(target, flags=flags)

    def get_affordances(self):
        raise NotImplementedError

    def get_ac_transfer_pairs(self):
        raise NotImplementedError


class PhoneAffordanceRegistration(_AffordanceRegistrationBase):

    def __init__(self, target=AffordanceTargetType.PHONE, flags=AffordanceFlagType.NONE):
        super().__init__(target, flags=flags)

    def get_affordances(self):
        raise NotImplementedError

    def test(self, omutsu_sim: OmutsuSim):
        raise NotImplementedError


class RelationshipPanelAffordanceRegistration(_AffordanceRegistrationBase):

    def __init__(self, target=AffordanceTargetType.RELATIONSHIP_PANEL, flags=AffordanceFlagType.NONE):
        super().__init__(target, flags=flags)

    def get_affordances(self):
        raise NotImplementedError

    def test(self, omutsu_sim: OmutsuSim):
        raise NotImplementedError


class EnvironmentAffordanceRegistration(_AffordanceRegistrationBase):

    def __init__(self, target=AffordanceTargetType.ALL_ENVIRONMENT, flags=AffordanceFlagType.NONE):
        super().__init__(target, flags=flags)

    def get_affordances(self):
        raise NotImplementedError


class MixerAffordanceRegistration(_AffordanceRegistrationBase):

    def __init__(self, target=AffordanceTargetType.MIXER):
        super().__init__(target)

    def get_affordances(self):
        raise NotImplementedError

    def get_affordance_lists(self):
        raise NotImplementedError


class SocialMixerAffordanceRegistration(_AffordanceRegistrationBase):
    DEFAULT_AFFORDANCE_LISTS = (24513, 163715)

    def __init__(self, target=AffordanceTargetType.SOCIAL_MIXER):
        super().__init__(target)

    def get_affordances(self):
        raise NotImplementedError

    def get_affordance_lists(self):
        return self.DEFAULT_AFFORDANCE_LISTS


class BuffAffordanceRegistration(_AffordanceRegistrationBase):

    def __init__(self, target=AffordanceTargetType.BUFF, destination=AffordanceProviderDestinationType.SI_ACTOR):
        super().__init__(target)
        self.destination = destination

    def get_affordances(self):
        raise NotImplementedError

    def get_buffs(self):
        raise NotImplementedError


class TraitAffordanceRegistration(_AffordanceRegistrationBase):

    def __init__(self, target=AffordanceTargetType.TRAIT, destination=AffordanceProviderDestinationType.SI_ACTOR):
        super().__init__(target)
        self.destination = destination

    def get_affordances(self):
        raise NotImplementedError

    def get_traits(self):
        raise NotImplementedError


@inject(GameObject, "on_add")
def _omutsulib_on_game_object_addition(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        get_affordances_service().add_object_affordances(self)
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run GameObject interaction injection at 'GameObject.on_add'.", ex)
        finally:
            ex = None
            del ex

    return result


@inject(TerrainService, "start")
def _omutsulib_on_terrain_object_creation(original, *args, **kwargs):
    try:
        terrain_definition = getattr(TerrainService, "TERRAIN_DEFINITION", None)
        if terrain_definition is not None:
            get_affordances_service().add_environment_affordances((terrain_definition.cls), target=(AffordanceTargetType.TERRAIN))
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run TerrainService interaction injection for target type TERRAIN.", ex)
        finally:
            ex = None
            del ex

    try:
        get_affordances_service().add_miscellaneous_affordances()
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run TerrainService interaction injection for miscellaneous affordances.", ex)
        finally:
            ex = None
            del ex

    return original(*args, **kwargs)


@inject(TerrainService, "on_zone_load")
def _omutsulib_on_ocean_object_creation(original, *args, **kwargs):
    try:
        ocean_definition = getattr(TerrainService, "OCEAN_DEFINITION", None)
        if ocean_definition is not None:
            get_affordances_service().add_environment_affordances((ocean_definition.cls), target=(AffordanceTargetType.WATER))
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run TerrainService interaction injection for target type WATER.", ex)
        finally:
            ex = None
            del ex

    return original(*args, **kwargs)


@inject(InstanceManager, "load_data_into_class_instances")
def _omutsulib_on_tunable_class_tuning_load(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        if self.TYPE == OmutsuResourceType.SNIPPET:
            affordance_list_instances = {}
            for (key, cls) in tuple(self._tuned_classes.items()):
                affordance_list_instances[key.instance] = (issubclass(cls, AFFORDANCE_LIST_CLASS)) if (inspect.isclass(cls)) else (issubclass(type(cls), AFFORDANCE_LIST_CLASS)) if (AFFORDANCE_LIST_CLASS is not None) else cls

            if affordance_list_instances:
                get_affordances_service().add_mixer_affordances(affordance_list_instances)
        elif self.TYPE == OmutsuResourceType.BUFF:
            buff_instances = {}
            for (key, cls) in tuple(self._tuned_classes.items()):
                buff_instances[key.instance] = cls

            if buff_instances:
                get_affordances_service().add_buff_affordances(buff_instances)
        elif self.TYPE == OmutsuResourceType.TRAIT:
            trait_instances = {}
            for (key, cls) in tuple(self._tuned_classes.items()):
                trait_instances[key.instance] = cls

            if trait_instances:
                get_affordances_service().add_trait_affordances(trait_instances)
    except Exception as ex:
        try:
            pass  # log_custom_exception("[OmutsuLib] Failed to run tunable class interaction injection at 'InstanceManager.load_data_into_class_instances'.", ex)
        finally:
            ex = None
            del ex

    return result
