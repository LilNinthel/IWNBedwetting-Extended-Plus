from autonomy.content_sets import get_valid_aops_gen
from interactions import PipelineProgress
from interactions.context import InteractionContext
from omutsulib.services.interactions_service import OmutsuPriority, OmutsuQueueInsertStrategy, OmutsuFinishingType, OmutsuInteractionContext
from omutsulib.services.resources_service import OmutsuResourceType, get_resource_service
from omutsulib.wrappers.interaction import OmutsuInteraction
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim


class _OmutsuSimInteractionMixin(_SuperOmutsuSim):

    def get_posture(self):
        sim = self.get_sim_instance()
        if sim is not None:
            posture = sim.posture
            if posture is not None:
                return getattr(posture, 'guid64', 0)
            return None

    def get_source_interaction(self):
        sim = self.get_sim_instance()
        if sim is not None:
            posture = sim.posture
            if posture is not None and posture.source_interaction is not None:
                return OmutsuInteraction(sim.posture.source_interaction.super_affordance)
            return None

    def is_interaction_running(self=None, *, ignore_finishing, affordance_ids):
        pass
        # sim = self.get_sim_instance()
        # if sim is not None and sim.si_state is not None:
        #     return None((lambda .0 = None: pass)(sim.si_state))

    def get_running_omutsu_interactions(self, ignore_finishing, filter_affordance_ids=(False, None)):
        sim = self.get_sim_instance()
        if sim is not None and sim.si_state is not None:
            interactions = []
            for interaction in sim.si_state:
                if not ignore_finishing:
                    if not interaction.is_finishing or filter_affordance_ids is None:
                        if getattr(interaction, 'guid64', None) in filter_affordance_ids:
                            interactions.append(OmutsuInteraction(interaction))
                        return interactions
                    return None

    def cancel_running_interaction(self=None, *, finishing_type, cancel_reason_msg, kill, affordance_ids):
        sim = self.get_sim_instance()
        if sim is not None and sim.si_state is not None:
            for si in list(sim.si_state):
                if not getattr(si, 'guid64', None) in affordance_ids or cancel_reason_msg:
                    pass
                si.cancel(finishing_type, 'iwnbedwetting.cancel_running_interaction')
                if kill:
                    return si.kill()

        return False

    def is_interaction_queued(self, *affordance_ids):
        pass
        # sim = self.get_sim_instance()
        # if sim is not None and sim.queue is not None:
        #     return None((lambda .0 = None: pass)(sim.queue))

    def get_queued_omutsu_interactions(self, filter_affordance_ids=(None,)):
        sim = self.get_sim_instance()
        if sim is not None and sim.queue is not None:
            interactions = []
            for interaction in sim.queue:
                if interaction.pipeline_progress > PipelineProgress.QUEUED:
                    continue
                if filter_affordance_ids is not None and getattr(interaction, 'guid64', None) not in filter_affordance_ids:
                    continue
                interactions.append(OmutsuInteraction(interaction))

            return interactions

    def cancel_queued_interaction(self=None, *, finishing_type, cancel_reason_msg, kill, affordance_ids):
        sim = self.get_sim_instance()
        if sim is not None and sim.queue is not None:
            for si in sim.queue:
                if not getattr(si, 'guid64', None) in affordance_ids or cancel_reason_msg:
                    pass
                si.cancel(finishing_type, 'iwnbedwetting.cancel_queued_interaction')
                if kill:
                    return si.kill()

        return False

    def set_queue_lock_state(self, state):
        sim = self.get_sim_instance()
        if sim is not None and sim.queue is not None:
            if not state:
                sim.queue.unlock()
            else:
                sim.queue.lock()

    def apply_pressure_to_interactions_queue(self):
        sim = self.get_sim_instance()
        if sim is not None and sim.queue is not None:
            sim.queue._apply_next_pressure()

    def push_affordance(self, affordance_id, social_super_affordance_id, target, interaction_context, priority, run_priority, insert_strategy, must_run_next, skip_if_running=(None, None, OmutsuInteractionContext.SOURCE_SCRIPT_WITH_USER_INTENT, OmutsuPriority.High, None, OmutsuQueueInsertStrategy.LAST, False, False), **kwargs):
        sim = self.get_sim_instance()
        if sim is None and sim.si_state is None and sim.queue is None and sim.posture_state is None or sim.posture is None:
            return None
        affordance = None().get_instance(OmutsuResourceType.INTERACTION, affordance_id)
        if affordance is None:
            return None
        if None:
            for si in sim.si_state:
                if si.super_affordance == affordance:
                    return None

            for si in sim.queue:
                if si.super_affordance == affordance:
                    return None

        if run_priority is None:
            run_priority = priority

    # WARNING: Decompyle incomplete

    def _push_super_affordance(self, affordance, target, interaction_context, priority, run_priority, insert_strategy, must_run_next=(None, OmutsuInteractionContext.SOURCE_SCRIPT_WITH_USER_INTENT, OmutsuPriority.High, OmutsuPriority.High, OmutsuQueueInsertStrategy.NEXT, False), **kwargs):
        sim = self.get_sim_instance()
        context = InteractionContext(sim, interaction_context, priority, run_priority, insert_strategy, must_run_next, **('run_priority', 'insert_strategy', 'must_run_next'))

    # WARNING: Decompyle incomplete

    def _push_mixer_affordance(self, mixer_affordance, target, social_super_affordance_id, interaction_context, priority, run_priority, insert_strategy, must_run_next=(None, OmutsuInteractionContext.SOURCE_SCRIPT_WITH_USER_INTENT, OmutsuPriority.High, OmutsuPriority.High, OmutsuQueueInsertStrategy.NEXT, False), **kwargs):
        sim = self.get_sim_instance()
        if sim is None and sim.si_state is None and sim.queue is None and sim.posture_state is None or sim.posture is None:
            return None
        if None is not None:
            social_super_affordance = get_resource_service().get_instance(OmutsuResourceType.INTERACTION, social_super_affordance_id)
        else:
            social_super_affordance = None
        if social_super_affordance is not None:
            push_super_on_prepare = True
            source_interaction = None
            source_affordance = social_super_affordance
            for super_interaction in sim.running_interactions_gen(social_super_affordance):
                source_interaction = super_interaction
                push_super_on_prepare = False

        else:
            push_super_on_prepare = False
            source_interaction = sim.posture.source_interaction
            if source_interaction is None:
                return None
            source_affordance = None.super_affordance
        for social_group in sim.get_groups_for_sim_gen():
            if social_group.disallow_reaction_mixers:
                return None

        sim_specific_lockout = mixer_affordance.lock_out_time.target_based_lock_out if mixer_affordance.lock_out_time is not None else False
        if sim_specific_lockout and sim.is_sub_action_locked_out(mixer_affordance):
            return None
        targets = None
        if target is not None:
            targets.append(target)
        elif source_interaction is not None:
            potential_targets = source_interaction.get_potential_mixer_targets()
            targets.extend(mixer_affordance.filter_mixer_targets(source_interaction, potential_targets, sim))
        if run_priority is None:
            run_priority = priority
        context = InteractionContext(sim, interaction_context, priority, run_priority, insert_strategy, must_run_next, **('run_priority', 'insert_strategy', 'must_run_next'))
        for target in targets:
            for aop, test_result in get_valid_aops_gen(target, mixer_affordance, source_affordance, source_interaction, context, False, push_super_on_prepare, kwargs, **('push_super_on_prepare', 'aop_kwargs')):
                if test_result:
                    interaction_constraint = aop.constraint_intersection(sim, None, **('sim', 'posture_state'))
                    posture_constraint = sim.posture_state.posture_constraint_strict
                    constraint_intersection = interaction_constraint.intersect(posture_constraint)
                    if constraint_intersection.valid:
                        mixer_result = aop.execute(context)
                        if mixer_result or sim.queue.always_start_inertial:
                            running_interaction = sim.queue.running
                            if not running_interaction is not None and running_interaction.is_super:
                                running_interaction.cancel(OmutsuFinishingType.DISPLACED, 'Reaction displaced mixer.', **('cancel_reason_msg',))
                return mixer_result




