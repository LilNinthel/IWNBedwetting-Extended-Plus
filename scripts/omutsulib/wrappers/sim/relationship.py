import services
from services.relgraph_service import RelgraphService
from omutsulib.services.resources_service import get_resource_service, OmutsuResourceType
from omutsulib.wrappers.enum import OmutsuIntEnum, OmutsuIntFlagsEnum
from omutsulib.wrappers.sim.super_sim import _SuperOmutsuSim, sim_info_required

class OmutsuSimRelBitShift(OmutsuIntEnum):
    SIMRELEBITSHIFT_MOTHER = 0
    SIMRELEBITSHIFT_FATHER = 1
    SIMRELEBITSHIFT_DAUGHTER = 2
    SIMRELEBITSHIFT_SON = 3
    SIMRELEBITSHIFT_WIFE = 4
    SIMRELEBITSHIFT_HUSBAND = 5
    SIMRELEBITSHIFT_MAX = 5
    SIMRELEBITSHIFT_PREEXISTING = 31


class OmutsuSimRelBitFlags(OmutsuIntFlagsEnum):
    SIMRELBITFLAG_NONE = 0
    SIMRELBITFLAG_MOTHER = 1 << OmutsuSimRelBitShift.SIMRELEBITSHIFT_MOTHER
    SIMRELBITFLAG_FATHER = 1 << OmutsuSimRelBitShift.SIMRELEBITSHIFT_FATHER
    SIMRELBITFLAG_DAUGHTER = 1 << OmutsuSimRelBitShift.SIMRELEBITSHIFT_DAUGHTER
    SIMRELBITFLAG_SON = 1 << OmutsuSimRelBitShift.SIMRELEBITSHIFT_SON
    SIMRELBITFLAG_WIFE = 1 << OmutsuSimRelBitShift.SIMRELEBITSHIFT_WIFE
    SIMRELBITFLAG_HUSBAND = 1 << OmutsuSimRelBitShift.SIMRELEBITSHIFT_HUSBAND
    SIMRELBITFLAG_PREEXISTING = 1 << OmutsuSimRelBitShift.SIMRELEBITSHIFT_PREEXISTING
    SIMRELBITS_MALE = SIMRELBITFLAG_FATHER | SIMRELBITFLAG_SON | SIMRELBITFLAG_HUSBAND
    SIMRELBITS_FEMALE = SIMRELBITFLAG_MOTHER | SIMRELBITFLAG_DAUGHTER | SIMRELBITFLAG_WIFE
    SIMRELBITS_CHILD = SIMRELBITFLAG_DAUGHTER | SIMRELBITFLAG_SON
    SIMRELBITS_PARENT = SIMRELBITFLAG_MOTHER | SIMRELBITFLAG_FATHER
    SIMRELBITS_SPOUSE = SIMRELBITFLAG_WIFE | SIMRELBITFLAG_HUSBAND
    SIMRELBITS_ALL = SIMRELBITS_CHILD | SIMRELBITS_PARENT | SIMRELBITS_SPOUSE


class _OmutsuSimRelationshipMixin(_SuperOmutsuSim):

    @sim_info_required(default=False)
    def set_relationship_score(self, sim_identifier, relationship_track_id, score, create=True):
        relationship_track_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, relationship_track_id)
        if relationship_track_instance is not None:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            target_omutsu_sim = OmutsuSim(sim_identifier)
            if target_omutsu_sim is not None:
                if self.get_sim_id() != target_omutsu_sim.get_sim_id():
                    relationship = services.relationship_service()._find_relationship((self.get_sim_id()), (target_omutsu_sim.get_sim_id()), create=create)
                    if relationship is not None:
                        relationship.set_relationship_score((self.get_sim_id()), score, track=relationship_track_instance)
                        return True
            return False

    @sim_info_required(default=False)
    def change_relationship_score(self, sim_identifier, relationship_track_id, score, apply_cross_age_multipliers=True, create=True):
        relationship_track_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, relationship_track_id)
        if relationship_track_instance is not None:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            target_omutsu_sim = OmutsuSim(sim_identifier)
            if target_omutsu_sim is not None:
                if self.get_sim_id() != target_omutsu_sim.get_sim_id():
                    relationship = services.relationship_service()._find_relationship((self.get_sim_id()), (target_omutsu_sim.get_sim_id()), create=create)
                    if relationship is not None:
                        relationship.add_track_score((self.get_sim_id()), score, relationship_track_instance, apply_cross_age_multipliers=apply_cross_age_multipliers)
                        return True
            return False

    @sim_info_required(default=0.0)
    def get_relationship_score(self, sim_identifier, relationship_track_id, default=0):
        relationship_track_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, relationship_track_id)
        if relationship_track_instance is not None:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            target_omutsu_sim = OmutsuSim(sim_identifier)
            if target_omutsu_sim is not None and self.get_sim_id() != target_omutsu_sim.get_sim_id():
                relationship = services.relationship_service()._find_relationship(self.get_sim_id(), target_omutsu_sim.get_sim_id())
                if relationship is not None:
                    return relationship.get_track_score(self.get_sim_id(), relationship_track_instance)
                if hasattr(relationship_track_instance, "get_initial_value"):
                    initial_value = relationship_track_instance.get_initial_value() / 1
                else:
                    initial_value = relationship_track_instance.default_value / 1
                if initial_value.is_integer():
                    return int(initial_value)
                return initial_value
            return default

    @sim_info_required(default=False)
    def remove_relationship_score(self, sim_identifier, relationship_track_id, notify_client=True, send_rel_change_event=True):
        relationship_track_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, relationship_track_id)
        if relationship_track_instance is not None:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            target_omutsu_sim = OmutsuSim(sim_identifier)
            if target_omutsu_sim is not None:
                relationship = services.relationship_service()._find_relationship(self.get_sim_id(), target_omutsu_sim.get_sim_id())
                if relationship is not None:
                    relationship.remove_track((self.get_sim_id()), (target_omutsu_sim.get_sim_id()), relationship_track_instance, notify_client=notify_client, send_rel_change_event=send_rel_change_event)
                    return True
            return False

    @sim_info_required(default=False)
    def is_family_relationship(self, sim_identifier):
        sim_info_family_data = self.get_sim_info().get_family_sim_ids(include_self=True)
        if sim_info_family_data:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            target_omutsu_sim = OmutsuSim(sim_identifier)
            target_sim_info_family_data = target_omutsu_sim.get_sim_info().get_family_sim_ids(include_self=True)
            if target_sim_info_family_data:
                families_union = set(sim_info_family_data) & set(target_sim_info_family_data)
                families_union.discard(None)
                if families_union:
                    return True
                return services.relationship_service().get_is_considered_incest(self.get_sim_id(), target_omutsu_sim.get_sim_id())
            return False

    @sim_info_required(default=False)
    def has_relationship_bit(self, sim_identifier, *relationship_bit_ids):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        target_omutsu_sim = OmutsuSim(sim_identifier)
        sim_relationship_bit_ids = {relationship_bit.guid64 for relationship_bit in services.relationship_service().get_all_bits((self.get_sim_id()), target_sim_id=(target_omutsu_sim.get_sim_id() if target_omutsu_sim is not None else None))}
        return not set(relationship_bit_ids).isdisjoint(sim_relationship_bit_ids)

    @sim_info_required(default=())
    def get_relationship_bits(self, sim_identifier):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        target_omutsu_sim = OmutsuSim(sim_identifier)
        return [relationship_bit for relationship_bit in services.relationship_service().get_all_bits((self.get_sim_id()), target_sim_id=(target_omutsu_sim.get_sim_id() if target_omutsu_sim is not None else None))]

    @sim_info_required(default=False)
    def add_relationship_bit(self, sim_identifier, *relationship_bit_ids, update_client=True, send_rel_change_event=True, refresh=False, force=False):
        relationship_bit_instances = {get_resource_service().get_instance(OmutsuResourceType.RELATIONSHIP_BIT, relationship_bit_id) for relationship_bit_id in relationship_bit_ids}
        relationship_bit_instances.discard(None)
        if relationship_bit_instances:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            target_omutsu_sim = OmutsuSim(sim_identifier)
            if target_omutsu_sim is not None:
                with services.relationship_service().suppress_client_updates_context_manager():
                    for relationship_bit_instance in relationship_bit_instances:
                        services.relationship_service().add_relationship_bit((self.get_sim_id()), (target_omutsu_sim.get_sim_id()), bit_to_add=relationship_bit_instance, force_add=force, from_load=False, send_rel_change_event=send_rel_change_event, allow_readdition=refresh)

                if update_client:
                    services.relationship_service().send_relationship_info((self.get_sim_id()), target_sim_id=(target_omutsu_sim.get_sim_id()))
                return True
            return False

    @sim_info_required(default=False)
    def remove_relationship_bit(self, sim_identifier, *relationship_bit_ids, update_client=True, send_rel_change_event=True):
        relationship_bit_instances = {get_resource_service().get_instance(OmutsuResourceType.RELATIONSHIP_BIT, relationship_bit_id) for relationship_bit_id in relationship_bit_ids}
        relationship_bit_instances.discard(None)
        if relationship_bit_instances:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            target_omutsu_sim = OmutsuSim(sim_identifier)
            if target_omutsu_sim is not None:
                with services.relationship_service().suppress_client_updates_context_manager():
                    for relationship_bit_instance in relationship_bit_instances:
                        services.relationship_service().remove_relationship_bit((self.get_sim_id()), (target_omutsu_sim.get_sim_id()), relationship_bit_instance, send_rel_change_event=send_rel_change_event)

                if update_client:
                    services.relationship_service().send_relationship_info((self.get_sim_id()), target_sim_id=(target_omutsu_sim.get_sim_id()))
                return True
            return False

    @sim_info_required()
    def update_client_relationship(self, sim_identifier):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        target_omutsu_sim = OmutsuSim(sim_identifier)
        if target_omutsu_sim is not None:
            relationship = services.relationship_service()._find_relationship(self.get_sim_id(), target_omutsu_sim.get_sim_id())
            if relationship is not None:
                relationship.send_relationship_info()

    @sim_info_required()
    def get_sims_with_relationship_bit_gen(self, *relationship_bit_ids):
        relationship_bit_instances = {get_resource_service().get_instance(OmutsuResourceType.RELATIONSHIP_BIT, relationship_bit_id) for relationship_bit_id in relationship_bit_ids}
        relationship_bit_instances.discard(None)
        if relationship_bit_instances:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            for relationship in services.relationship_service().get_all_sim_relationships(self.get_sim_id()):
                if relationship.sim_id_a != self.get_sim_id():
                    target_sim_id = relationship.sim_id_a
                else:
                    target_sim_id = relationship.sim_id_b
                if any((relationship.has_bit(self.get_sim_id(), relationship_bit_instance) for relationship_bit_instance in relationship_bit_instances)):
                    target_omutsu_sim = OmutsuSim(target_sim_id)
                    if target_omutsu_sim is not None:
                        yield target_omutsu_sim

    @sim_info_required(default=0)
    def get_all_relationships_count(self):
        return len(services.relationship_service().get_all_sim_relationships(self.get_sim_id()))

    @sim_info_required()
    def get_all_relationship_sims_gen(self):
        from omutsulib.wrappers.sim.sim import OmutsuSim
        for relationship in services.relationship_service().get_all_sim_relationships(self.get_sim_id()):
            if relationship.sim_id_a != self.get_sim_id():
                target_sim_id = relationship.sim_id_a
            else:
                target_sim_id = relationship.sim_id_b
            target_omutsu_sim = OmutsuSim(target_sim_id)
            if target_omutsu_sim is not None:
                yield target_omutsu_sim

    def set_relgraph_edge(self, target_sim_id, relationship_type):
        RelgraphService.relgraph_set_edge(self.get_sim_id(), target_sim_id, relationship_type)

    def set_relgraph_marriage(self, spouse_sim_id, is_married):
        RelgraphService.relgraph_set_marriage(self.get_sim_id(), spouse_sim_id, is_married)

    def set_relgraph_child(self, parent_a_id, parent_b_id):
        RelgraphService.relgraph_add_child(parent_a_id, parent_b_id, self.get_sim_id())
