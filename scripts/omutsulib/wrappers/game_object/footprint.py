import placement
from placement import get_accurate_placement_footprint_polygon
from omutsulib.wrappers.game_object.super_game_object import _SuperOmutsuGameObject

class _OmutsuObjectFootprintMixin(_SuperOmutsuGameObject):

    def get_footprint_state(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            obj_footprint_comp = object_instance.footprint_component
            if obj_footprint_comp is not None:
                return obj_footprint_comp.footprints_enabled
            return True

    def set_footprint_state(self, state):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            obj_footprint_comp = object_instance.footprint_component
            if obj_footprint_comp is not None:
                if state:
                    obj_footprint_comp.enable_footprint(force_enable=True)
                else:
                    obj_footprint_comp.disable_footprint(force_disable=True)

    def get_footprint_height(self):
        object_instance = self.get_object_instance()
        if object_instance is not None and hasattr(object_instance, "footprint"):
            footprint = object_instance.footprint
            if footprint is not None:
                try:
                    return placement.get_object_height(footprint)
                except ValueError:
                    pass

                return 0.0

    def get_footprint_outline_polygon(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            try:
                return list(get_accurate_placement_footprint_polygon(object_instance.position, object_instance.orientation, object_instance.scale, object_instance.get_footprint()))
            except:
                pass

            return ()
