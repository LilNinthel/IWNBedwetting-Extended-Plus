from buffs.buff import Buff
from omutsulib.services.components_service import get_components_service, OmutsuComponentType
from omutsulib.services.l18n_service import get_l18n_service
from omutsulib.services.resources_service import get_resource_service, OmutsuResourceType
from omutsulib.services.time_service import get_time_service
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class _OmutsuSimBuffMixin(_SuperOmutsuSim):

    @sim_info_required(default=0)
    def get_mood(self):
        return self.get_sim_info().get_mood().guid64

    @sim_info_required(default=False)
    def has_mood(self, *mood_ids):
        return self.get_sim_info().get_mood().guid64 in set(mood_ids)

    @sim_info_required(default=False)
    def has_buff(self, *buff_ids):
        buff_component = get_components_service().get_object_component(self.get_sim_info(), OmutsuComponentType.BUFF)
        if not buff_component:
            return False
        sim_buff_ids = {getattr(buff_entry, "guid64", 0) for buff_entry in buff_component}
        return not set(buff_ids).isdisjoint(sim_buff_ids)

    @sim_info_required(default=())
    def get_buffs(self):
        buff_component = get_components_service().get_object_component(self.get_sim_info(), OmutsuComponentType.BUFF)
        if not buff_component:
            return ()
        return [buff_instance for buff_instance in buff_component if buff_instance is not None if isinstance(buff_instance, Buff) if buff_instance is not None if isinstance(buff_instance, Buff)]

    @sim_info_required(default=False)
    def add_buff(self, buff_id, buff_reason=None, refresh=True):
        if not get_components_service().has_object_component(self.get_sim_info(), OmutsuComponentType.BUFF):
            return False
        buff_instance = get_resource_service().get_instance(OmutsuResourceType.BUFF, buff_id)
        if buff_instance is None:
            return False
        if not refresh:
            if buff_instance in self.get_sim_info().get_active_buff_types():
                return False
        if buff_reason is not None:
            buff_reason = get_l18n_service().get_localized_string(buff_reason)
        return self.get_sim_info().add_buff_from_op(buff_instance, buff_reason=buff_reason)

    @sim_info_required(default=False)
    def remove_buff(self, *buff_ids):
        buff_component = get_components_service().get_object_component(self.get_sim_info(), OmutsuComponentType.BUFF)
        if not buff_component:
            return False
        buff_ids = set(buff_ids)
        buff_entries = [buff_entry for buff_entry in buff_component if getattr(buff_entry, "guid64", 0) in buff_ids]
        for buff_entry in buff_entries:
            self.get_sim_info().remove_buff_entry(buff_entry)

        return True

    @sim_info_required(default=False)
    def remove_all_mood_buffs(self, mood_id, required_tags=None):
        buff_component = get_components_service().get_object_component(self.get_sim_info(), OmutsuComponentType.BUFF)
        if not buff_component:
            return False
        if required_tags is not None:
            required_tags = set(required_tags)
        buff_entries = [buff_entry for buff_entry in buff_component if buff_entry.mood_type is not None if buff_entry.mood_type.guid64 == mood_id if required_tags if buff_entry.has_any_tag(required_tags)]
        for buff_entry in buff_entries:
            self.get_sim_info().remove_buff_entry(buff_entry)

        return True

    @sim_info_required(default=False)
    def add_delayed_buff(self, buff_id, buff_reason=None, refresh=True, timeout=15000):
        if self.get_sim_instance() is not None:
            return self.add_buff(buff_id, buff_reason=buff_reason, refresh=refresh)
        if not get_components_service().has_object_component(self.get_sim_info(), OmutsuComponentType.BUFF):
            return False
        buff_instance = get_resource_service().get_instance(OmutsuResourceType.BUFF, buff_id)
        if buff_instance is None:
            return False
        delayed_buffs = self.get_temp_value("delayed_buffs") or {}
        delayed_buff_entry = (buff_id, buff_reason, refresh, get_time_service().get_absolute_ticks() + timeout)
        delayed_buffs[buff_id] = delayed_buff_entry
        self.set_temp_value("delayed_buffs", delayed_buffs)
        return True

    @sim_info_required(default=False)
    def remove_delayed_buff(self, *buff_ids):
        buff_component = get_components_service().get_object_component(self.get_sim_info(), OmutsuComponentType.BUFF)
        if not buff_component:
            return False
        delayed_buffs = self.get_temp_value("delayed_buffs")
        if delayed_buffs:
            for buff_id in buff_ids:
                if buff_id is not None:
                    delayed_buffs.pop(buff_id, None)

        return True

    def _handle_delayed_buff_on_instance_spawn(self):
        delayed_buffs = self.get_temp_value("delayed_buffs")
        if delayed_buffs:
            for (buff_identifier, buff_reason, refresh, timeout) in delayed_buffs.values():
                if get_time_service().get_absolute_ticks() < timeout:
                    self.add_buff(buff_identifier, buff_reason=buff_reason, refresh=refresh)

            delayed_buffs.clear()

    @sim_info_required()
    def register_on_buff_added_callback(self, callback):
        buff_component = get_components_service().get_object_component(self.get_sim_info(), OmutsuComponentType.BUFF)
        if buff_component:
            if callback not in buff_component.on_buff_added:
                buff_component.on_buff_added.append(callback)

    @sim_info_required()
    def unregister_on_buff_added_callback(self, callback):
        buff_component = get_components_service().get_object_component(self.get_sim_info(), OmutsuComponentType.BUFF)
        if buff_component:
            if callback in buff_component.on_buff_added:
                buff_component.on_buff_added.remove(callback)

    @sim_info_required()
    def register_on_buff_removed_callback(self, callback):
        buff_component = get_components_service().get_object_component(self.get_sim_info(), OmutsuComponentType.BUFF)
        if buff_component:
            if callback not in buff_component.on_buff_removed:
                buff_component.on_buff_removed.append(callback)

    @sim_info_required()
    def unregister_on_buff_removed_callback(self, callback):
        buff_component = get_components_service().get_object_component(self.get_sim_info(), OmutsuComponentType.BUFF)
        if buff_component:
            if callback in buff_component.on_buff_removed:
                buff_component.on_buff_removed.remove(callback)
