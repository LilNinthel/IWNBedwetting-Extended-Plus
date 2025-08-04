import services
from element_utils import build_element
from omutsulib.services.components_service import OmutsuComponentType, get_components_service
from omutsulib.wrappers.game_object.super_game_object import _SuperOmutsuGameObject

class _OmutsuObjectInventoryMixin(_SuperOmutsuGameObject):

    def get_inventory_stack_count(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.stack_count()
        return 1

    def get_inventory_objects(self):
        object_instance = self.get_object_instance()
        if object_instance is None:
            return ()
        inventory_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.INVENTORY)
        if inventory_component:
            return tuple(inventory_component)
        return ()

    def add_inventory_object(self, game_object):
        object_instance = self.get_object_instance()
        if object_instance is None:
            return False
        inventory_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.INVENTORY)
        if inventory_component:
            return inventory_component.player_try_add_object(game_object)
        return False

    def remove_inventory_object(self, game_object, count=1, destroy=True):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            timeline = services.time_service().sim_timeline
            inventory_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.INVENTORY)
            if inventory_component is not None:
                from omutsulib.wrappers.game_object.game_object import OmutsuGameObject
                omutsu_game_object = OmutsuGameObject(game_object)
                elements = [
                 (lambda _: inventory_component.try_remove_object_by_id((omutsu_game_object.get_object_id()), count=count))]
                if destroy:
                    elements.append(lambda _: omutsu_game_object.destroy(cause="Inventory removal."))
                element = build_element(elements)
                timeline.schedule(element)
                return True
            return False

    def count_inventory_objects_with_definition(self, object_definition):
        object_instance = self.get_object_instance()
        if object_instance is None:
            return 0
        inventory_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.INVENTORY)
        if inventory_component:
            return inventory_component.get_count(object_definition)
        return 0
