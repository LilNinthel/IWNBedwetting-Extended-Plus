from cas.cas import get_tags_from_outfit
from protocolbuffers import S4Common_pb2, Outfits_pb2, PersistenceBlobs_pb2
from sims.occult.occult_enums import OccultType
from sims.outfits.outfit_tuning import OutfitTuning
from omutsulib.services.cas_service import OmutsuOutfitCategory, OmutsuBodyType, OmutsuCasPart, OmutsuOutfitOverrideOptionFlag, OmutsuAppearanceModifierPriority
from omutsulib.tunables.tunable_types import OmutsuSingleSimResolver
from omutsulib.utils.math import random_int_of_bit_length
from omutsulib.utils.singletons import EMPTY_DICT
from omutsulib.wrappers.enum import OmutsuIntEnum
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class _OmutsuSimCASMixin(_SuperOmutsuSim):

    @sim_info_required(default=(0, 0), base_wrapper=True)
    def get_current_outfit(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return sim_info.get_current_outfit()

    @sim_info_required(base_wrapper=True)
    def set_current_outfit(self, outfit_category_and_index, dirty=False):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        if dirty:
            sim_info.set_outfit_dirty(outfit_category_and_index[0])
        return sim_info.set_current_outfit(outfit_category_and_index)

    @sim_info_required()
    def apply_outfit_changed_loot(self):
        sim_info = self.get_sim_info()
        resolver = OmutsuSingleSimResolver(sim_info)
        for loot_action in OutfitTuning.LOOT_ON_OUTFIT_CHANGE:
            loot_action.apply_to_resolver(resolver)

    @sim_info_required(default=(0, 0), base_wrapper=True)
    def get_previous_outfit(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return sim_info.get_previous_outfit() or (OmutsuOutfitCategory.EVERYDAY, 0)

    @sim_info_required(base_wrapper=True)
    def set_previous_outfit(self, outfit_category_and_index):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info._previous_outfit = outfit_category_and_index

    @sim_info_required(base_wrapper=True)
    def refresh_previous_outfit(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info.set_previous_outfit(None)

    @sim_info_required(default=False, base_wrapper=True)
    def has_outfit(self, outfit_category_and_index):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        try:
            return sim_info.has_outfit(outfit_category_and_index)
        except:
            return False

    @sim_info_required(base_wrapper=True)
    def generate_outfit(self, outfit_category_and_index):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info.generate_outfit(outfit_category_and_index[0], outfit_category_and_index[1])

    @sim_info_required(base_wrapper=True)
    def set_outfit_category_dirty(self, outfit_category, state):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        if state:
            sim_info.set_outfit_dirty(outfit_category)
        else:
            sim_info.clear_outfit_dirty(outfit_category)

    @sim_info_required(base_wrapper=True)
    def register_on_outfit_changed_callback(self, callback):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info.register_for_outfit_changed_callback(callback)

    @sim_info_required(base_wrapper=True)
    def unregister_on_outfit_changed_callback(self, callback):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info.unregister_for_outfit_changed_callback(callback)

    @sim_info_required(base_wrapper=True)
    def get_change_outfit_element(self, outfit_category_and_index, do_spin=False, interaction=None, dirty_outfit=False):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        if dirty_outfit:
            sim_info.set_outfit_dirty(outfit_category_and_index[0])
        return sim_info.get_change_outfit_element(outfit_category_and_index, do_spin=do_spin, interaction=interaction)

    @sim_info_required(default=EMPTY_DICT, base_wrapper=True)
    def get_outfit_tags(self, outfit_category_index, body_type_filter=OmutsuBodyType.NONE):
        try:
            return get_tags_from_outfit((self.get_sim_info()._base), (outfit_category_index[0]), (outfit_category_index[1]), body_type_filter=body_type_filter)
        except:
            return EMPTY_DICT

    @sim_info_required(default=EMPTY_DICT, base_wrapper=True)
    def get_outfit_parts(self, outfit_category_and_index):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        outfit_data = sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])
        if outfit_data is None:
            return EMPTY_DICT
        outfit_id = getattr(outfit_data, 'outfit_id', -1)
        outfits_msg = sim_info.save_outfits()
        outfit_data_msg = next(iter((outfit for outfit in outfits_msg.outfits if outfit.category == outfit_category_and_index[0] and outfit.outfit_id == outfit_id)), None)
        if outfit_data_msg is None:
            return EMPTY_DICT
        body_types = list(outfit_data_msg.body_types_list.body_types)
        cas_parts = list(outfit_data_msg.parts.ids)
        color_shifts = list(outfit_data_msg.part_shifts.color_shift)
        object_ids = list(outfit_data_msg.object_ids.object_id)
        layer_ids = list(outfit_data_msg.layer_ids.layer_id)
        outfit_parts = {}
        for (i, body_type) in enumerate(body_types):
            cas_part = OmutsuCasPart((cas_parts[i]), color_shift=(color_shifts[i]), object_id=(object_ids[i]), layer_id=(layer_ids[i]))
            if body_type not in outfit_parts:
                outfit_parts[body_type] = (cas_part,)
            else:
                if not isinstance(outfit_parts[body_type], tuple):
                    outfit_parts[body_type] = (
                     outfit_parts[body_type],)
                outfit_parts[body_type] += (cas_part,)

        return outfit_parts

    @sim_info_required(default=EMPTY_DICT, base_wrapper=True)
    def get_outfit_parts_without_color_shift(self, outfit_category_and_index):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        outfit_data = sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])
        if outfit_data is None:
            return EMPTY_DICT
        outfits_msg = sim_info.save_outfits()
        outfit_data_msg = next(iter((outfit for outfit in outfits_msg.outfits)), None)
        if outfit_data_msg is None:
            return EMPTY_DICT
        body_types = list(outfit_data_msg.body_types_list.body_types)
        cas_parts = list(outfit_data_msg.parts.ids)
        outfit_parts = {}
        for (i, body_type) in enumerate(body_types):
            if body_type not in outfit_parts:
                outfit_parts[body_type] = cas_parts[i]
            else:
                if not isinstance(outfit_parts[body_type], tuple):
                    outfit_parts[body_type] = (
                     outfit_parts[body_type],)
                outfit_parts[body_type] += (cas_parts[i],)

        return outfit_parts

    @sim_info_required(base_wrapper=True)
    def set_outfit_parts(self, outfit_category_and_index, outfit_parts, keep_current_outfit=False):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        outfit_data = sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])
        if outfit_data is None:
            return
        outfit_body_types = []
        outfit_part_ids = []
        outfit_color_shifts = []
        outfit_object_ids = []
        outfit_layer_ids = []
        for (body_type, cas_part_or_seq) in outfit_parts.items():
            if body_type == -1:
                continue
            if isinstance(cas_part_or_seq, tuple):
                if not cas_part_or_seq:
                    continue
            elif cas_part_or_seq.cas_part == -1:
                continue
            else:
                cas_part_or_seq = (
                 cas_part_or_seq,)
            for cas_part in cas_part_or_seq:
                if cas_part.cas_part == -1:
                    continue
                outfit_body_types.append(body_type)
                outfit_part_ids.append(cas_part.cas_part)
                outfit_color_shifts.append(cas_part.color_shift)
                outfit_object_ids.append(cas_part.object_id)
                outfit_layer_ids.append(cas_part.layer_id)

        outfits_msg = sim_info.save_outfits()
        outfit_id = getattr(sim_info.get_outfit(outfit_category_and_index[0],outfit_category_and_index[1]), 'outfit_id', -1)
        # getattr(sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1]), 'outfit_id', -1)

        for outfit in outfits_msg.outfits:
            if outfit.category != int(outfit_category_and_index[0]):
                # logger.info("wrong outfit category. expected {} got {}",outfit_category_and_index[0], outfit.category)
                continue
            if outfit.outfit_id != outfit_id:
                # logger.info("wrong outfit id. expected {} got {}",outfit_id, outfit.outfit_id)
                continue
            else:
                outfit.parts = S4Common_pb2.IdList()
                outfit.parts.ids.extend(outfit_part_ids)
                outfit.body_types_list = Outfits_pb2.BodyTypesList()
                outfit.body_types_list.body_types.extend(outfit_body_types)
                outfit.part_shifts = Outfits_pb2.ColorShiftList()
                outfit.part_shifts.color_shift.extend(outfit_color_shifts)
                outfit.object_ids = Outfits_pb2.ObjectIdsList()
                outfit.object_ids.object_id.extend(outfit_object_ids)
                outfit.layer_ids = Outfits_pb2.LayerIdsList()
                outfit.layer_ids.layer_id.extend(outfit_layer_ids)
                break
        sim_info._base.outfits = outfits_msg.SerializeToString()
        # logger.info('outfit {}', sim_info._base.outfits)
        # if not keep_current_outfit:
        sim_info._base.outfit_type_and_index = outfit_category_and_index
        # sim_info.set_outfit_dirty(outfit_category_and_index[0])
        sim_info.resend_outfits()


        # outfits_msg = sim_info.save_outfits()
        # outfit_data_msg = next(iter((outfit for outfit in outfits_msg.outfits)), None)
        # if outfit_data_msg is None:
        #     return
        # outfit_data_msg.parts = S4Common_pb2.IdList()
        # outfit_data_msg.parts.ids.extend(outfit_part_ids)
        # outfit_data_msg.body_types_list = Outfits_pb2.BodyTypesList()
        # outfit_data_msg.body_types_list.body_types.extend(outfit_body_types)
        # outfit_data_msg.part_shifts = Outfits_pb2.ColorShiftList()
        # outfit_data_msg.part_shifts.color_shift.extend(outfit_color_shifts)
        # outfit_data_msg.object_ids = Outfits_pb2.ObjectIdsList()
        # outfit_data_msg.object_ids.object_id.extend(outfit_object_ids)
        # outfit_data_msg.layer_ids = Outfits_pb2.LayerIdsList()
        # outfit_data_msg.layer_ids.layer_id.extend(outfit_layer_ids)
        # sim_info._base.outfits = outfits_msg.SerializeToString()
        # if keep_current_outfit:
        #     sim_info._base.outfit_type_and_index = outfit_category_and_index

    @sim_info_required(default=None, base_wrapper=True)
    def get_outfit_id(self, outfit_category_and_index):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        outfit_data = sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])
        if outfit_data is not None:
            return outfit_data.outfit_id
        return -1

    @sim_info_required()
    def regenerate_outfit_ids(self):
        sim_info = self.get_sim_info()
        current_outfit_category_and_index = self.get_current_outfit()
        occult_sim_infos = [
         sim_info]
        for occult_type in OccultType:
            occult_sim_info = sim_info.occult_tracker.get_occult_sim_info(occult_type)
            if occult_sim_info is not None:
                if occult_sim_info not in occult_sim_infos:
                    occult_sim_infos.append(occult_sim_info)

        for occult_sim_info in occult_sim_infos:
            outfits_msg = occult_sim_info.save_outfits()
            outfit_ids = set()
            regenerate = False
            for outfit in outfits_msg.outfits:
                if outfit.outfit_id not in outfit_ids:
                    outfit_ids.add(outfit.outfit_id)
                else:
                    regenerate = True
                    break

            if regenerate:
                new_outfit_id_base = random_int_of_bit_length(60)
                for outfit in outfits_msg.outfits:
                    outfit.outfit_id = new_outfit_id_base
                    new_outfit_id_base += 1

            occult_sim_info._base.outfits = outfits_msg.SerializeToString()

        sim_info.resend_outfits()
        self.set_current_outfit(current_outfit_category_and_index, dirty=True)

    @sim_info_required(base_wrapper=True)
    def get_outfits_data(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return sim_info.save_outfits()

    @sim_info_required(base_wrapper=True)
    def resend_outfits_data(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info.resend_outfits()

    @sim_info_required(base_wrapper=True)
    def refresh_outfits_data(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info.on_outfit_changed(self.get_sim_info(), self.get_sim_info().get_current_outfit(), None)
        sim_info.resend_outfits()
        sim_info.appearance_tracker.evaluate_appearance_modifiers()


class _OmutsuSimAppearanceModifiersMixin(_SuperOmutsuSim):

    @sim_info_required(base_wrapper=True)
    def has_any_appearance_modifiers(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return bool(sim_info.appearance_tracker._active_appearance_modifier_infos)

    @sim_info_required(base_wrapper=True)
    def has_appearance_modifiers(self, guid):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        appearance_tracker = sim_info.appearance_tracker
        if appearance_tracker._active_appearance_modifier_infos:
            for appearance_modifier_list in appearance_tracker._active_appearance_modifier_infos.values():
                if any((appearance_modifier_info.guid == guid for appearance_modifier_info in appearance_modifier_list)):
                    return True

        return False

    @sim_info_required(base_wrapper=True)
    def has_appearance_modifiers_tag(self, tag):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        appearance_tracker = sim_info.appearance_tracker
        if appearance_tracker._active_appearance_modifier_infos:
            for appearance_modifier_list in appearance_tracker._active_appearance_modifier_infos.values():
                if any((appearance_modifier_info.modifier.appearance_modifier_tag == tag for appearance_modifier_info in appearance_modifier_list)):
                    return True

        return False

    @sim_info_required(base_wrapper=True)
    def add_appearance_modifier(self, modifier, guid, priority=OmutsuAppearanceModifierPriority.TRANSFORMED, apply_to_all_outfits=True, additional_flags=OmutsuOutfitOverrideOptionFlag.DEFAULT):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        appearance_tracker = sim_info.appearance_tracker
        if isinstance(modifier, tuple):
            if len(modifier) > 1:
                modifier = appearance_tracker._choose_modifier(modifier)
            else:
                modifier = modifier[0].modifier
        return appearance_tracker.add_appearance_modifier(modifier, guid, priority, apply_to_all_outfits, additional_flags=additional_flags)

    @sim_info_required(base_wrapper=True)
    def remove_appearance_modifiers(self, guid):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        appearance_tracker = sim_info.appearance_tracker
        if appearance_tracker._active_appearance_modifier_infos:
            keys_to_remove = []
            for (mod_type, appearance_modifier_list) in appearance_tracker._active_appearance_modifier_infos.items():
                modifier_infos_to_remove = []
                for appearance_modifier_info in appearance_modifier_list:
                    if appearance_modifier_info.guid == guid:
                        modifier_infos_to_remove.append(appearance_modifier_info)

                if modifier_infos_to_remove:
                    appearance_tracker._active_appearance_modifier_infos[mod_type] = [mod for mod in appearance_tracker._active_appearance_modifier_infos[mod_type] if mod not in modifier_infos_to_remove]
                    if not appearance_tracker._active_appearance_modifier_infos[mod_type]:
                        keys_to_remove.append(mod_type)

            for mod_type in keys_to_remove:
                appearance_tracker._active_appearance_modifier_infos.pop(mod_type, None)

            appearance_tracker.remove_persistent_appearance_modifier_data(guid)

    @sim_info_required(base_wrapper=True)
    def evaluate_appearance_modifiers(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        appearance_tracker = sim_info.appearance_tracker
        appearance_tracker.evaluate_appearance_modifiers()
        if appearance_tracker.appearance_override_sim_info is not None:
            sim_instance = self.get_sim_instance()
            if sim_instance is not None:
                sim_instance.apply_outfit_buffs_for_sim_info(appearance_tracker.appearance_override_sim_info, sim_info.get_current_outfit())

    @sim_info_required(default=EMPTY_DICT)
    def get_appearance_modifiers_outfit_parts(self, outfit_category_and_index):
        sim_info = self.get_sim_info()
        sim_info_base_wrapper = sim_info.appearance_tracker.appearance_override_sim_info
        if sim_info_base_wrapper is None:
            return EMPTY_DICT
        outfit_data = sim_info_base_wrapper.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])
        if outfit_data is None:
            return EMPTY_DICT
        outfits_msg = sim_info_base_wrapper.save_outfits()
        outfit_data_msg = next(iter((outfit for outfit in outfits_msg.outfits)), None)
        if outfit_data_msg is None:
            return EMPTY_DICT
        body_types = list(outfit_data_msg.body_types_list.body_types)
        cas_parts = list(outfit_data_msg.parts.ids)
        color_shifts = list(outfit_data_msg.part_shifts.color_shift)
        object_ids = list(outfit_data_msg.object_ids.object_id)
        layer_ids = list(outfit_data_msg.layer_ids.layer_id)
        outfit_parts = {}
        for (i, body_type) in enumerate(body_types):
            cas_part = OmutsuCasPart((cas_parts[i]), color_shift=(color_shifts[i]), object_id=(object_ids[i]), layer_id=(layer_ids[i]))
            if body_type not in outfit_parts:
                outfit_parts[body_type] = cas_part
            else:
                if not isinstance(outfit_parts[body_type], tuple):
                    outfit_parts[body_type] = (
                     outfit_parts[body_type],)
                outfit_parts[body_type] += (cas_part,)

        return outfit_parts

    @sim_info_required(default=EMPTY_DICT)
    def get_appearance_modifiers_outfit_parts_without_color_shift(self, outfit_category_and_index):
        sim_info = self.get_sim_info()
        sim_info_base_wrapper = sim_info.appearance_tracker.appearance_override_sim_info
        if sim_info_base_wrapper is None:
            return EMPTY_DICT
        outfit_data = sim_info_base_wrapper.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])
        if outfit_data is None:
            return EMPTY_DICT
        outfits_msg = sim_info_base_wrapper.save_outfits()
        outfit_data_msg = next(iter((outfit for outfit in outfits_msg.outfits)), None)
        if outfit_data_msg is None:
            return EMPTY_DICT
        body_types = list(outfit_data_msg.body_types_list.body_types)
        cas_parts = list(outfit_data_msg.parts.ids)
        outfit_parts = {}
        for (i, body_type) in enumerate(body_types):
            if body_type not in outfit_parts:
                outfit_parts[body_type] = cas_parts[i]
            else:
                if not isinstance(outfit_parts[body_type], tuple):
                    outfit_parts[body_type] = (
                     outfit_parts[body_type],)
                outfit_parts[body_type] += (cas_parts[i],)

        return outfit_parts

    @sim_info_required(default=(), base_wrapper=True)
    def get_appearance_modifiers(self, *appearance_modifier_types, guid=None):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        modifiers = {}
        if sim_info is None or sim_info.appearance_tracker._active_appearance_modifier_infos is None:
            return modifiers
        for appearance_modifier_type in appearance_modifier_types:
            if appearance_modifier_type not in sim_info.appearance_tracker._active_appearance_modifier_infos:
                continue
            else:
                for appearance_modifier in sim_info.appearance_tracker._active_appearance_modifier_infos[appearance_modifier_type]:
                    if guid is not None:
                        if appearance_modifier.guid != guid:
                            continue
                        if not appearance_modifier.should_display:
                            continue
                        else:
                            modifiers[appearance_modifier.guid] = appearance_modifier.modifier

        return modifiers

    @sim_info_required(base_wrapper=True)
    def register_on_appearance_tracker_changed_callback(self, callback):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        if callback not in sim_info.appearance_tracker_changed:
            sim_info.appearance_tracker_changed.append(callback)

    @sim_info_required(base_wrapper=True)
    def unregister_on_appearance_tracker_changed_callback(self, callback):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        if callback in sim_info.appearance_tracker_changed:
            sim_info.appearance_tracker_changed.remove(callback)


class OmutsuPhysiqueBodyBlendIndex(OmutsuIntEnum):
    BODY_BLEND_TYPE_HEAVY = 0
    BODY_BLEND_TYPE_FIT = 1
    BODY_BLEND_TYPE_LEAN = 2
    BODY_BLEND_TYPE_BONY = 3
    BODY_BLEND_TYPE_PREGNANT = 4
    BODY_BLEND_TYPE_HIPS_WIDE = 5
    BODY_BLEND_TYPE_HIPS_NARROW = 6
    BODY_BLEND_TYPE_WAIST_WIDE = 7
    BODY_BLEND_TYPE_WAIST_NARROW = 8


class OmutsuSimModifierType(OmutsuIntEnum):
    INVALID = 0
    EYES = 1
    NOSE = 2
    MOUTH = 3
    CHEEKS = 4
    CHIN = 5
    JAW = 6
    FOREHEAD = 7
    BROWS = 8
    EARS = 9
    HEAD = 10
    FULL_FACE = 11
    CHEST = 12
    UPPER_CHEST = 13
    NECK = 14
    SHOULDERS = 15
    UPPER_ARM = 16
    LOWER_ARM = 17
    HANDS = 18
    WAIST = 19
    HIPS = 20
    BELLY = 21
    BUTT = 22
    THIGHS = 23
    LOWER_LEG = 24
    FEET = 25
    BODY = 26
    UPPER_BODY = 27
    LOWER_BODY = 28
    TAIL = 29
    FUR = 30
    FORELEGS = 31
    HINDLEGS = 32


class _OmutsuSimAppearanceAttributesMixin(_SuperOmutsuSim):

    @sim_info_required(default=0, base_wrapper=True)
    def get_skin_tone(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return int(sim_info.skin_tone)

    @sim_info_required(base_wrapper=True)
    def set_skin_tone(self, skin_tone):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info.skin_tone = skin_tone
        sim_info.resend_skin_tone()

    @sim_info_required(default=(), base_wrapper=True)
    def get_physique(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        physique = []
        for body_blend in sim_info.physique.split(","):
            try:
                bb = float(body_blend)
            except:
                bb = body_blend

            physique.append(bb)

        return physique

    @sim_info_required(base_wrapper=True)
    def set_physique(self, physique, update_fitness=True):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info.physique = ",".join([str(body_blend) for body_blend in physique])
        if update_fitness:
            sim_info._get_fit_fat()
            sim_info._setup_fitness_commodities()
        sim_info.resend_physique()

    @sim_info_required(default=0, base_wrapper=True)
    def get_voice_pitch(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return sim_info.voice_pitch

    @sim_info_required(base_wrapper=True)
    def set_voice_pitch(self, voice_pitch):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info.voice_pitch = voice_pitch
        sim_info.resend_voice_pitch()

    @sim_info_required(default=0, base_wrapper=True)
    def get_voice_actor(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return sim_info.voice_actor

    @sim_info_required(base_wrapper=True)
    def set_voice_actor(self, voice_actor):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info.voice_actor = voice_actor
        sim_info.resend_voice_actor()

    @sim_info_required(default=0, base_wrapper=True)
    def get_voice_effect(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        return sim_info.voice_effect

    @sim_info_required(base_wrapper=True)
    def set_voice_effect(self, voice_effect):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        sim_info.voice_effect = voice_effect
        sim_info.resend_voice_effect()

    @sim_info_required(default=EMPTY_DICT, base_wrapper=True)
    def get_appearance_attributes(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        appearance_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
        appearance_attributes.ParseFromString(sim_info.facial_attributes)
        appearance_attributes_data = {}
        appearance_attributes_data["face_modifiers"] = dict([(modifier.key, modifier.amount) for modifier in appearance_attributes.face_modifiers])
        appearance_attributes_data["body_modifiers"] = dict([(modifier.key, modifier.amount) for modifier in appearance_attributes.body_modifiers])
        appearance_attributes_data["sculpts"] = [sculpt for sculpt in appearance_attributes.sculpts]
        return appearance_attributes_data

    @sim_info_required(base_wrapper=True)
    def set_appearance_attributes(self, appearance_attributes_data, override=False):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        current_appearance_attributes = None
        new_appearance_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
        if override:
            current_appearance_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
            current_appearance_attributes.ParseFromString(sim_info.facial_attributes)
        if "face_modifiers" in appearance_attributes_data or override:
            face_modifiers = {} if current_appearance_attributes is None else dict([(modifier.key, modifier.amount) for modifier in current_appearance_attributes.face_modifiers])
            face_modifiers.update(appearance_attributes_data.get("face_modifiers", EMPTY_DICT))
            for (key, value) in face_modifiers.items():
                new_modifier = new_appearance_attributes.face_modifiers.add()
                new_modifier.key = key
                new_modifier.amount = value

        if "body_modifiers" in appearance_attributes_data or override:
            body_modifiers = {} if current_appearance_attributes is None else dict([(modifier.key, modifier.amount) for modifier in current_appearance_attributes.body_modifiers])
            body_modifiers.update(appearance_attributes_data.get("body_modifiers", EMPTY_DICT))
            for (key, value) in body_modifiers.items():
                new_modifier = new_appearance_attributes.body_modifiers.add()
                new_modifier.key = key
                new_modifier.amount = value

        if "sculpts" in appearance_attributes_data or override:
            sculpts = [] if current_appearance_attributes is None else [sculpt for sculpt in current_appearance_attributes.sculpts]
            for sculpt in appearance_attributes_data.get("sculpts", ()):
                if sculpt not in sculpts:
                    sculpts.append(sculpt)

            new_appearance_attributes.sculpts.extend(sculpts)
        sim_info.facial_attributes = new_appearance_attributes.SerializeToString()
        sim_info.resend_facial_attributes()

    @sim_info_required(base_wrapper=True)
    def update_genetic_data(self):
        sim_info = self.get_sim_info_base() or self.get_sim_info()
        genetic_data = Outfits_pb2.GeneticData()
        genetic_data.ParseFromString(sim_info.genetic_data)
        genetic_data.sculpts_and_mods_attr = sim_info.facial_attributes
        genetic_data.physique = sim_info.physique
        genetic_data.voice_pitch = sim_info.voice_pitch
        genetic_data.voice_actor = sim_info.voice_actor
        genetic_data.parts_list = Outfits_pb2.PartDataList()
        genetic_data.growth_parts_list = Outfits_pb2.PartDataList()
        outfit_data = sim_info.get_outfit(OmutsuOutfitCategory.EVERYDAY, 0)
        if outfit_data is not None:
            outfit_parts = dict(zip(list(outfit_data.body_types), list(outfit_data.part_ids)))
            for body_type in OmutsuBodyType.get_all_non_clothing_body_types():
                if body_type in outfit_parts:
                    part_data = Outfits_pb2.PartData()
                    part_data.body_type = int(body_type)
                    part_data.id = int(outfit_parts[body_type])
                    genetic_data.parts_list.parts.append(part_data)

        sim_info.genetic_data = genetic_data.SerializeToString()
        sim_info.resend_genetic_data()

    @sim_info_required()
    def resend_appearance_attributes(self):
        self.get_sim_info().resend_physical_attributes()
