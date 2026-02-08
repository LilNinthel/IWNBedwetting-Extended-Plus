import _buildbuy, services
from animation.posture_manifest import Hand
from carry.carry_utils import is_wing_proxy_object
from interactions.si_state import SIState
from objects.object_enums import ResetReason
from postures import posture_graph
from postures.posture_specs import get_origin_spec, PostureSpecVariable
from postures.posture_state import PostureState
from omutsulib.services.interactions_service import OmutsuFinishingType
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class OmutsuSimLODLevel:
    MINIMUM = 1
    BACKGROUND = 10
    BASE = 25
    INTERACTED = 50
    FULL = 100
    ACTIVE = 125


class _OmutsuSimInternalMixin(_SuperOmutsuSim):

    def is_instanced(self):
        return self.get_sim_instance() is not None

    @sim_info_required(default=True)
    def is_npc(self):
        return self.get_sim_info().is_npc

    @sim_info_required(default=False)
    def is_player(self):
        return not self.get_sim_info().is_npc

    @sim_info_required(default=False)
    def is_selected(self):
        return self.get_sim_info().is_selected

    @sim_info_required(default=False)
    def is_premade(self):
        return self.get_sim_info().is_premade_sim

    @sim_info_required(default=True)
    def get_lod_level(self):
        return self.get_sim_info().lod

    @sim_info_required(default=True)
    def set_lod_level(self, lod_level):
        return self.get_sim_info().request_lod(lod_level)

    @sim_info_required()
    def remove(self):
        self.get_sim_info().remove_permanently()

    @sim_info_required(default=None)
    def get_creation_source(self):
        return getattr(self.get_sim_info().creation_source, "creation_source_data", None)

    def destroy(self, cause=None):
        sim = self.get_sim_instance()
        if sim is not None:
            sim.destroy(cause=cause)

    def is_visible(self):
        if services.hidden_sim_service().is_hidden(self.get_sim_id()):
            return False
        sim = self.get_sim_instance()
        if sim is not None:
            if sim.is_hidden():
                return False
        return True

    def add_game_tags(self, *tags, persist=False):
        sim = self.get_sim_instance()
        if sim is not None:
            sim.append_tags((set(tags)), persist=persist)

    def remove_game_tags(self, *tags):
        sim = self.get_sim_instance()
        if sim is not None:
            tags = set(tags)
            dynamic_tags = sim.get_dynamic_tags()
            if tags & dynamic_tags:
                try:
                    sim.remove_dynamic_tags(tags)
                except KeyError:
                    pass

    def get_visibility_flags(self):
        sim = self.get_sim_instance()
        if sim is not None:
            visibility_flags = sim.visibility_flags
            if visibility_flags is not None:
                return visibility_flags
        return 255

    def set_visibility_flags(self, value):
        sim = self.get_sim_instance()
        if sim is not None:
            sim.visibility_flags = value

    def fade_in(self, fade_duration=1.0, immediate=False):
        sim = self.get_sim_instance()
        if sim is not None:
            sim.fade_in(fade_duration=fade_duration, immediate=immediate)

    def fade_out(self, fade_duration=1.0, immediate=False):
        sim = self.get_sim_instance()
        if sim is not None:
            sim.fade_out(fade_duration=fade_duration, immediate=immediate)

    def hard_reset(self):
        sim = self.get_sim_instance()
        if sim is None:
            return True
        try:
            self.get_sim_instance().reset(ResetReason.RESET_EXPECTED)
            return True
        except:
            return False

    def soft_reset(self, hard_reset_on_exception=False):
        sim = self.get_sim_instance()
        if sim is None:
            return True
        try:
            if sim._should_be_swimming() or _buildbuy.is_location_pool(services.current_zone_id(), sim.position, sim.location.level):
                posture_type = posture_graph.SIM_SWIM_POSTURE_TYPE
            else:
                posture_type = posture_graph.SIM_DEFAULT_POSTURE_TYPE
            if sim.queue is not None:
                for interaction in sim.queue:
                    interaction.cancel((OmutsuFinishingType.KILLED), "OmutsuLib: soft_reset", immediate=True, ignore_must_run=True)

                sim.queue.on_reset()
                sim.queue.unlock()
            if sim.si_state is not None:
                for interaction in list(sim.si_state):
                    interaction.cancel((OmutsuFinishingType.KILLED), "OmutsuLib: soft_reset", immediate=True, ignore_must_run=True)

                try:
                    sim.si_state.on_reset()
                except:
                    sim._si_state = SIState(sim)
                    sim.si_state.on_reset()

            else:
                sim._si_state = SIState(sim)
                sim.si_state.on_reset()
            if sim.ui_manager is not None:
                sim.ui_manager.remove_all_interactions()
            sim.socials_locked = False
            sim.last_affordance = None
            sim.two_person_social_transforms.clear()
            sim.on_reset_send_op(ResetReason.RESET_EXPECTED)
            if sim.posture_state is not None:
                posture_back = sim.posture_state.back
                if posture_back is not None:
                    posture_source = posture_back.source_interaction
                    if posture_source is not None:
                        posture_source.cancel(finishing_type=(OmutsuFinishingType.KILLED), cancel_reason_msg="OmutsuLib: soft_reset", immediate=True, ignore_must_run=True)
                    posture_back_target = posture_back.target
                    if posture_back_target is not None:
                        if is_wing_proxy_object(posture_back_target):
                            posture_back_target.destroy(source=sim, cause="OmutsuLib: soft_reset")
                        if sim.posture_state._primitive is not None:
                            sim.posture_state._primitive._prev_posture = None
                    sim.posture_state.on_reset(ResetReason.RESET_EXPECTED)
            sim._stop_animation_interaction()
            sim.asm_auto_exit.clear()
            sim._start_animation_interaction()
            try:
                sim.posture_state = PostureState(sim, None, get_origin_spec(posture_type), {(PostureSpecVariable.HAND): (Hand.LEFT,)})
            except:
                sim.posture_state = PostureState(sim, None, get_origin_spec(posture_graph.SIM_DEFAULT_POSTURE_TYPE), {(PostureSpecVariable.HAND): (Hand.LEFT,)})

            sim._posture_target_refs.clear()
            sim.run_full_autonomy_next_ping()
            return True
        except:
            if hard_reset_on_exception:
                return self.hard_reset()

        return False
