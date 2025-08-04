import weakref
from collections import namedtuple
from date_and_time import TimeSpan
from interactions.priority import can_displace
from omutsulib.services.interactions_service import OmutsuFinishingType, OmutsuInteractionContext
from omutsulib.services.world_service import get_zone_service
from omutsulib.utils.math import SurfaceIdentifier
from omutsulib.utils.singletons import ZERO_VECTOR3
from omutsulib.wrappers.wrappers_manager import OmutsuInstance
_OmutsuInteractionInfo = namedtuple("_OmutsuInteraction", ('sim', 'target', 'source',
                                                         'affordance_tags'))

def _create_omutsu_interaction(interaction):
    return _OmutsuInteractionInfo(interaction.sim, interaction.target, interaction.source, interaction.get_category_tags())


OmutsuInteractionInfo = _create_omutsu_interaction

class _SuperOmutsuInteraction(OmutsuInstance):

    def __init__(self, interaction):
        super().__init__(None)
        self._interaction = weakref.ref(interaction)

    def __new__(cls, interaction):
        if interaction is None:
            return
        return super().__new__(cls)

    def get_interaction_instance(self):
        return self._interaction()

    def get_sim(self):
        interaction = self.get_interaction_instance()
        if interaction is not None:
            return interaction.sim

    def get_target(self):
        interaction = self.get_interaction_instance()
        if interaction is not None:
            return interaction.target

    def get_participants(self, participant_type):
        interaction = self.get_interaction_instance()
        if interaction is not None:
            return interaction.get_participants(participant_type)
        return ()

    def get_affordance_tags(self):
        interaction = self.get_interaction_instance()
        if interaction is not None:
            return interaction.get_category_tags()
        return ()

    def get_start_time(self):
        interaction = self.get_interaction_instance()
        if interaction is not None:
            return interaction.start_time
        return TimeSpan(0)

    def get_source(self):
        interaction = self.get_interaction_instance()
        if interaction is not None:
            return interaction.source
        return OmutsuInteractionContext.SOURCE_SCRIPT

    def get_guid(self):
        interaction = self.get_interaction_instance()
        if interaction is not None:
            return getattr(interaction, "guid64", 0)
        return 0

    def get_id(self):
        interaction = self.get_interaction_instance()
        if interaction is not None:
            return interaction.id
        return 0

    def cancel(self, finishing_type=OmutsuFinishingType.NATURAL, reason="OmutsuLib: _SuperOmutsuInteraction.cancel()"):
        interaction = self.get_interaction_instance()
        if interaction is not None:
            return interaction.cancel(finishing_type, reason)
        return False

    def kill(self):
        interaction = self.get_interaction_instance()
        if interaction is not None:
            return interaction.kill()
        return False

    def register_on_finishing_callback(self, callback):
        interaction = self.get_interaction_instance()
        if interaction is not None:
            if callback not in interaction._finisher._on_finishing_callbacks:
                interaction.register_on_finishing_callback(callback)

    def unregister_on_finishing_callback(self, callback):
        interaction = self.get_interaction_instance()
        if interaction is not None:
            interaction.unregister_on_finishing_callback(callback)


class OmutsuInteraction(_SuperOmutsuInteraction):

    def __init__(self, interaction):
        super().__init__(interaction)


def can_interaction_fallback_to_mixer_interaction(sim_identifier, interaction):
    if interaction is None:
        return True
    from omutsulib.wrappers.sim.sim import OmutsuSim
    omutsu_sim = OmutsuSim(sim_identifier)
    if omutsu_sim is None:
        return False
    sim = omutsu_sim.get_sim_instance()
    for running_interaction in sim.si_state:
        if running_interaction.is_guaranteed():
            continue
        if not can_displace(interaction, running_interaction):
            continue
        if not sim.si_state.are_sis_compatible(running_interaction, interaction):
            continue
        return True

    return False


def get_interaction_from_enqueue_result(enqueue_result):
    return enqueue_result.interaction


def get_interaction_context_position(interaction_context, location_object=None):
    if interaction_context.pick is not None:
        position = interaction_context.pick.location
        routing_surface = interaction_context.pick.routing_surface
        surface_height = get_zone_service().get_routing_surface_height_at(position.x, position.z, routing_surface)
        position.y = surface_height
        return position
    if location_object is not None:
        return location_object.position
    return ZERO_VECTOR3


def get_interaction_context_routing_surface(interaction_context, location_object=None):
    if interaction_context.pick is not None:
        return interaction_context.pick.routing_surface
    if location_object is not None:
        return location_object.location.routing_surface
    return SurfaceIdentifier(0)
