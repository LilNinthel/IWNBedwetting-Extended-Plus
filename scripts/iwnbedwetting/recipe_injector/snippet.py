import services
from crafting.recipe import Recipe
import sims4.log
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import HasTunableReferenceFactory, TunableSet, TunableReference, TunableMapping

import traceback

logger = sims4.log.Logger('RecipeInjector')


class RecipeInjector(HasTunableReferenceFactory, metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(Types.SNIPPET)):

    class MenuKey(TunableSet):

        def __init__(self, *arguments, **kwargs):
            args = {'description':'A list of crafting interactions to add recipes to', 
             'tunable':TunableReference(description='A list of menus to add recipes to',
               manager=services.get_instance_manager(Types.INTERACTION),
               reload_dependent=True,
               pack_safe=True)}
            (args.update)(**kwargs)
            (super().__init__)(*arguments, **args)

    class RecipeInjections(TunableSet):

        def __init__(self, *arguments, **kwargs):
            args = {'description':'A list of recipes to add to the crafting menu(s)', 
             'tunable':TunableReference(description='',
               manager=services.get_instance_manager(Types.RECIPE),
               pack_safe=True,
               class_restrictions=(
              Recipe,))}
            (args.update)(**kwargs)
            (super().__init__)(*arguments, **args)

    INSTANCE_TUNABLES = {'recipe_injections': TunableMapping(description='A mapping of crafting interactions to the recipe injections',
                            tuple_name='recipe_injections',
                            key_name='menu_ids',
                            key_type=(MenuKey()),
                            value_name='recipe_ids',
                            value_type=(RecipeInjections()))}

    @classmethod
    def _tuning_loaded_callback(cls) -> None:
        logger.info('Processing {}', str(cls))
        try:
            for menu_ids, recipes in cls.recipe_injections.items():
                for menu in menu_ids:
                    logger.info('  {}: adding recipes: {}', menu,
                                recipes)
                    recipe_list = list(menu.recipes)
                    recipe_list.extend(recipes)
                    menu.recipes = tuple(recipe_list)
        except:
            logger.error('Exception occurred processing RecipeInjector tuning instance {}', str(cls))
            logger.error(traceback.format_exc())

    def __repr__(self):
        return '<RecipeInjector:({})>'.format(self.__name__)

    def __str__(self):
        return '{}'.format(self.__name__)
