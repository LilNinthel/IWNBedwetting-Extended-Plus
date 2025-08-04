from omutsulib.wrappers.game_object.catalog import _OmutsuObjectCatalogMixin
from omutsulib.wrappers.game_object.footprint import _OmutsuObjectFootprintMixin
from omutsulib.wrappers.game_object.interactions import _OmutsuObjectInteractionsMixin
from omutsulib.wrappers.game_object.internal import _OmutsuObjectInternalMixin
from omutsulib.wrappers.game_object.inventory import _OmutsuObjectInventoryMixin
from omutsulib.wrappers.game_object.location import _OmutsuObjectLocationMixin
from omutsulib.wrappers.game_object.name import _OmutsuObjectNameMixin
from omutsulib.wrappers.game_object.portal import _OmutsuObjectPortalMixin
from omutsulib.wrappers.game_object.reservation import _OmutsuObjectReservationMixin
from omutsulib.wrappers.game_object.slots import _OmutsuObjectSlotMixin
from omutsulib.wrappers.game_object.state import _OmutsuObjectStateMixin
from omutsulib.wrappers.game_object.statistics import _OmutsuObjectStatisticsMixin
from omutsulib.wrappers.game_object.stored_sim import _OmutsuObjectStoredSimMixin
from omutsulib.wrappers.game_object.super_game_object import OmutsuGameObjectSingleton
from omutsulib.wrappers.game_object.tooltip import _OmutsuObjectTooltipMixin

class OmutsuGameObject(_OmutsuObjectInternalMixin, _OmutsuObjectLocationMixin, _OmutsuObjectFootprintMixin, _OmutsuObjectInventoryMixin, _OmutsuObjectCatalogMixin, _OmutsuObjectReservationMixin, _OmutsuObjectPortalMixin, _OmutsuObjectStateMixin, _OmutsuObjectSlotMixin, _OmutsuObjectStoredSimMixin, _OmutsuObjectInteractionsMixin, _OmutsuObjectStatisticsMixin, _OmutsuObjectTooltipMixin, _OmutsuObjectNameMixin, metaclass=OmutsuGameObjectSingleton):

    def __init__(self, *args, proxy_object=False):
        game_object_identifier = args[0]
        super().__init__(game_object_identifier, proxy_object=proxy_object)

    def __repr__(self):
        return type(self.get_object_instance()).__name__
