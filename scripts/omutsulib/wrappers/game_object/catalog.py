from omutsulib.utils.singletons import EMPTY_SET
from omutsulib.wrappers.game_object.super_game_object import _SuperOmutsuGameObject

class _OmutsuObjectCatalogMixin(_SuperOmutsuGameObject):

    def get_game_tags(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return object_instance.get_tags()
        return EMPTY_SET

    def add_game_tags(self, *tags, persist=False):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            object_instance.append_tags((set(tags)), persist=persist)

    def remove_game_tags(self, *tags):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            object_instance.remove_dynamic_tags(set(tags))
