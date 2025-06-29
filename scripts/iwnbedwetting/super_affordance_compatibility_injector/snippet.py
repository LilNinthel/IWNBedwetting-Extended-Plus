# import services
# import sims4.log
# from interactions.base.super_interaction import SuperInteraction
# from sims4.resources import Types
# from sims4.tuning.instances import HashedTunedInstanceMetaclass
# from sims4.tuning.tunable import HasTunableReference, TunableSet, TunableReference, TunableMapping, AutoFactoryInit, \
#     HasTunableReference, HasTunableSingletonFactory, Tunable, TunableTuple, TunableList, TunableReference, \
#     TunableVariant, TunableEnumEntry, OptionalTunable, TunableResourceKey
# import traceback
#
# from sims4.tuning.tunable_base import GroupNames
# from snippets import TunableVenueListReference, _TunableAffordanceFilter
#
# logger = sims4.log.Logger('ConsumableAffordanceInjector')
#
#
# class InteractionSelection(TunableVariant):
#     class _DefaultCompatibilityType(HasTunableSingletonFactory, AutoFactoryInit):
#         FACTORY_TUNABLES = {}
#
#         def get_objects(self):
#             # Iterate through all object tunings from the DefinitionManager
#             # and return those that contain the referenced affordance
#             obj_list = []
#             for tun in services.affordance_manager()._tuned_classes.values():
#                 if isinstance(tun, SuperInteraction):
#                     if hasattr(tun, 'super_affordance_compatibility'):
#                         if hasattr(tun.super_affordance_compatibility, 'default_inclusion'):
#                             if hasattr(tun.super_affordance_compatibility.default_inclusion, 'exclude_all'):
#                                 logger.info()
#             return obj_list
#
#     def __init__(self, **kwargs):
#         super().__init__(
#             objects_with_consumable_affordance=InteractionSelection._DefaultCompatibilityType.TunableFactory(),
#             default=None,
#             **kwargs)
#
#
# class SuperAffordanceCompatibilityInjector(HasTunableReference, metaclass=HashedTunedInstanceMetaclass,
#                                            manager=services.get_instance_manager(Types.SNIPPET)):
#     INSTANCE_TUNABLES = {
#         'super_affordance_compatibility_injector': TunableList(
#             description='A list of object and interaction lists',
#             tunable=TunableTuple(
#                 inclusion_type=InteractionSelection(),
#                 _super_affordances=TunableList(
#                     description='A list of consumable interactions to add to the objects',
#                     tunable=TunableReference(
#                         description='Reference to an interaction tuning instance',
#                         manager=services.affordance_manager(),
#                         class_restrictions=('SuperInteraction',),
#                         allow_none=False,
#                         pack_safe=True)
#                 )
#             ),
#             allow_none=False,
#             unique_entries=True
#         )
#     }
#
#     def add_consumable_affordances_to_objects(object_selection, sa_list):
#         logger.info('Starting add_consumable_affordances_to_objects')
#         for tun in object_selection.get_objects():
#             if hasattr(tun, '_components'):
#                 if hasattr(tun._components, 'consumable'):
#                     if hasattr(tun._components.consumable, 'consume_affordances'):
#                         sa_to_add_list = []
#                         for sa in sa_list:
#                             if not sa in tun._components.consumable.consume_affordances:
#                                 sa_to_add_list.append(sa)
#                         if len(sa_to_add_list) > 0:
#                             logger.info('  {}: adding _components.consumable.consume_affordances: {}', tun,
#                                         sa_to_add_list)
#                             tun._components.consumable._tuned_values = tun._components.consumable._tuned_values.clone_with_overrides(
#                                 consume_affordances=tun._components.consumable._tuned_values.consume_affordances + tuple(
#                                     sa_to_add_list))
#
#     @classmethod
#     def _tuning_loaded_callback(cls) -> None:
#         logger.info('Processing {}', str(cls))
#         try:
#             for entry in cls.add_consumable_interactions_to_objects:
#                 if isinstance(entry.object_selection, str) or entry.object_selection is None:
#                     logger.warn('Tuning warning, missing or invalid object_selection')
#                 else:
#                     SuperAffordanceCompatibilityInjector.add_consumable_affordances_to_objects(entry.object_selection,
#                                                                                        entry._super_affordances)
#         except:
#             logger.error('Exception occurred processing ConsumableAffordanceInjector tuning instance {}', str(cls))
#             logger.error(traceback.format_exc())
#
#     def __repr__(self):
#         return '<ConsumableAffordanceInjector:({})>'.format(self.__name__)
#
#     def __str__(self):
#         return '{}'.format(self.__name__)
