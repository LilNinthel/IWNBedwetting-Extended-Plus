import services
from element_utils import build_element
from omutsulib.services.components_service import OmutsuComponentType, get_components_service
from omutsulib.services.game_objects_service import get_game_objects_service
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim

class _OmutsuSimInventoryMixin(_SuperOmutsuSim):

    def get_inventory_objects(self):
        sim = self.get_sim_instance()
        if sim is not None:
            inventory_component = get_components_service().get_object_component(sim, OmutsuComponentType.INVENTORY)
            if inventory_component:
                return tuple(inventory_component)
            return ()

    def try_split_inventory_object_stack(self, object_identifier, count=1):
        sim = self.get_sim_instance()
        if sim is not None:
            from omutsulib.wrappers.game_object.game_object import OmutsuGameObject
            omutsu_game_object = OmutsuGameObject(object_identifier)
            if omutsu_game_object is not None:
                if omutsu_game_object.get_inventory_stack_count() > count:
                    inventory_component = get_components_service().get_object_component(sim, OmutsuComponentType.INVENTORY)
                    if inventory_component is not None:
                        new_obj = inventory_component.try_split_object_from_stack_by_id((omutsu_game_object.get_object_id()), count=count)
                        if new_obj is not None:
                            return OmutsuGameObject(new_obj)
                else:
                    return omutsu_game_object

    def create_inventory_object(self, object_definition, quantity=1):
        sim = self.get_sim_instance()
        sim_info = self.get_sim_info()
        created_objects = []
        if sim is not None:
            inventory_component = get_components_service().get_object_component(sim, OmutsuComponentType.INVENTORY)
            if inventory_component is not None:

                def _post_create(game_object):
                    game_object.update_ownership(sim_info, make_sim_owner=True)
                    inventory_component.player_try_add_object(game_object)

                for _ in range(quantity):
                    object_instance = get_game_objects_service().create_game_object(object_definition, post_add=_post_create)
                    if object_instance is not None:
                        created_objects.append(object_instance)

        elif sim_info is not None:

            def _post_create(game_object):
                game_object.update_ownership(sim_info, make_sim_owner=True)
                sim_info.try_add_object_to_inventory_without_component(game_object)

            for _ in range(quantity):
                object_instance = get_game_objects_service().create_game_object(object_definition, post_add=_post_create)
                if object_instance is not None:
                    created_objects.append(object_instance)

        return created_objects

    def add_inventory_object(self, game_object):
        sim = self.get_sim_instance()
        if sim is not None:
            inventory_component = get_components_service().get_object_component(sim, OmutsuComponentType.INVENTORY)
            if inventory_component is not None:
                game_object.update_ownership((sim.sim_info), make_sim_owner=True)
                return inventory_component.player_try_add_object(game_object)
            return False

    def remove_inventory_object(self, game_object, count=1, destroy=True):
        sim = self.get_sim_instance()
        if sim is not None:
            timeline = services.time_service().sim_timeline
            inventory_component = get_components_service().get_object_component(sim, OmutsuComponentType.INVENTORY)
            if inventory_component is not None:
                from omutsulib.wrappers.game_object.game_object import OmutsuGameObject
                omutsu_game_object = OmutsuGameObject(game_object)

                def _try_remove_object(_):
                    obj_id = omutsu_game_object.get_object_id()
                    if inventory_component.try_get_item_by_id(obj_id) is not None:
                        inventory_component.try_remove_object_by_id(obj_id, count=count)

                elements = [
                 _try_remove_object]
                if destroy:
                    elements.append(lambda _: omutsu_game_object.destroy(cause="Inventory removal."))
                element = build_element(elements)
                timeline.schedule(element)
                return True
            return False

    def count_inventory_objects_with_definition(self, object_definition):
        sim = self.get_sim_instance()
        if sim is not None:
            inventory_component = get_components_service().get_object_component(sim, OmutsuComponentType.INVENTORY)
            if inventory_component:
                return inventory_component.get_count(object_definition)
            return 0
