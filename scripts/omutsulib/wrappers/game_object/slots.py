import sims4.hash_util
from interactions.utils.parent_object import parent_object as parent_object
from omutsulib.services.components_service import get_components_service, OmutsuComponentType
from omutsulib.wrappers.game_object.super_game_object import _SuperOmutsuGameObject

class _OmutsuObjectSlotMixin(_SuperOmutsuGameObject):

    def get_parent_slot_hash(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            parent_object_instance = object_instance.location.parent
            if parent_object_instance is not None:
                slot_component = get_components_service().get_object_component(parent_object_instance, OmutsuComponentType.SLOT)
                if slot_component is not None:
                    for runtime_slot in slot_component.get_runtime_slots_gen():
                        children = runtime_slot.children
                        if children:
                            if object_instance in children:
                                return runtime_slot.slot_name_hash

            return 0

    def set_parent_slot(self, parent_object_instance, joint_name_or_hash=None):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            joint_name_hash = sims4.hash_util.hash32(joint_name_or_hash) if isinstance(joint_name_or_hash, str) else joint_name_or_hash
            parent_object(object_instance, parent_object_instance, bone_name_hash=joint_name_hash)

    def get_children_with_slot_hash(self, joint_name_or_hash):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            slot_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.SLOT)
            if slot_component is not None:
                joint_name_hash = sims4.hash_util.hash32(joint_name_or_hash) if isinstance(joint_name_or_hash, str) else joint_name_or_hash
                for runtime_slot in slot_component.get_runtime_slots_gen():
                    if runtime_slot.slot_name_hash == joint_name_hash:
                        children = runtime_slot.children
                        if children:
                            from omutsulib.wrappers.game_object.game_object import OmutsuGameObject
                            return [OmutsuGameObject(child_object_instance) for child_object_instance in children]

            return ()

    def get_all_slot_hashes(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            while object_instance.parent is not None:
                parent = object_instance.parent
                if parent is not None:
                    object_instance = parent
                else:
                    break

            slot_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.SLOT)
            if slot_component is not None:
                try:
                    return [slot_hash for slot_hash, _ in slot_component.get_containment_slot_infos()]
                except AttributeError:
                    pass

            return ()

    def get_all_slots_objects_gen(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            slot_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.SLOT)
            if slot_component is not None:
                for runtime_slot in slot_component.get_runtime_slots_gen():
                    children = runtime_slot.children
                    if children:
                        for child_object_instance in children:
                            from omutsulib.wrappers.game_object.game_object import OmutsuGameObject
                            yield (
                             runtime_slot.slot_name_hash, OmutsuGameObject(child_object_instance))

    def get_all_slot_types_objects_gen(self, slot_types=()):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            while object_instance.parent is not None:
                parent = object_instance.parent
                if parent is not None:
                    object_instance = parent
                else:
                    break

            slot_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.SLOT)
            if slot_component is not None:
                for runtime_slot in slot_component.get_runtime_slots_gen():
                    children = runtime_slot.children
                    if children:
                        if slot_types:
                            if any((slot_type.__name__ in slot_types for slot_type in runtime_slot.slot_types)):
                                pass
                            for child_object_instance in children:
                                from omutsulib.wrappers.game_object.game_object import OmutsuGameObject
                                yield (
                                 runtime_slot.slot_types, OmutsuGameObject(child_object_instance))

    def has_all_slot_types_empty(self, slot_types=()):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            while object_instance.parent is not None:
                parent = object_instance.parent
                if parent is not None:
                    object_instance = parent
                else:
                    break

            slot_component = get_components_service().get_object_component(object_instance, OmutsuComponentType.SLOT)
            if slot_component is not None:
                for runtime_slot in slot_component.get_runtime_slots_gen():
                    if not runtime_slot.empty:
                        if slot_types:
                            if any((slot_type.__name__ in slot_types for slot_type in runtime_slot.slot_types)):
                                pass
                            return False

            return True
        return False
