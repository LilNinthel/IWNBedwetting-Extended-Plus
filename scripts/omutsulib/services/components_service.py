import objects.components.types
from objects.components import ComponentContainer
from omutsulib.services.service import OmutsuService

class OmutsuComponentType:

    def _get_component_type(*args):
        try:
            return getattr(objects.components.types, args[0])
        except:
            return

    AFFORDANCE_TUNING = _get_component_type("AFFORDANCE_TUNING_COMPONENT")
    ANIMAL_HOME = _get_component_type("ANIMAL_HOME_COMPONENT")
    ANIMAL_OBJECT = _get_component_type("ANIMAL_OBJECT_COMPONENT")
    ANIMAL_PREFERENCE = _get_component_type("ANIMAL_PREFERENCE_COMPONENT")
    ANIMATION = _get_component_type("ANIMATION_COMPONENT")
    ANIMATION_OVERLAY = _get_component_type("ANIMATION_OVERLAY_COMPONENT")
    AUDIO = _get_component_type("AUDIO_COMPONENT")
    AUTONOMY = _get_component_type("AUTONOMY_COMPONENT")
    AUTONOMY_MARKER = _get_component_type("AUTONOMY_MARKER_COMPONENT")
    AWARENESS = _get_component_type("AWARENESS_COMPONENT")
    BRANDING_ICON = _get_component_type("BRANDING_ICON_COMPONENT")
    BUFF = _get_component_type("BUFF_COMPONENT")
    CAMERA_VIEW = _get_component_type("CAMERA_VIEW_COMPONENT")
    CANVAS = _get_component_type("CANVAS_COMPONENT")
    CARRYABLE = _get_component_type("CARRYABLE_COMPONENT")
    CARRYING = _get_component_type("CARRYING_COMPONENT")
    CENSOR_GRID = _get_component_type("CENSOR_GRID_COMPONENT")
    CHANNEL = _get_component_type("CHANNEL_COMPONENT")
    CHARGEABLE = _get_component_type("CHARGEABLE_COMPONENT")
    CHARGING_STATION = _get_component_type("CHARGING_STATION_COMPONENT")
    COLLECTABLE = _get_component_type("COLLECTABLE_COMPONENT")
    CONSUMABLE = _get_component_type("CONSUMABLE_COMPONENT")
    CRAFTING = _get_component_type("CRAFTING_COMPONENT")
    CRAFTING_STATION = _get_component_type("CRAFTING_STATION_COMPONENT")
    CURFEW = _get_component_type("CURFEW_COMPONENT")
    DISPLAY = _get_component_type("DISPLAY_COMPONENT")
    EFFECTS = _get_component_type("EFFECTS_COMPONENT")
    ENSEMBLE = _get_component_type("ENSEMBLE_COMPONENT")
    ENVIRONMENT_SCORE = _get_component_type("ENVIRONMENT_SCORE_COMPONENT")
    EXAMPLE = _get_component_type("EXAMPLE_COMPONENT")
    FISHING_LOCATION = _get_component_type("FISHING_LOCATION_COMPONENT")
    FLOWING_PUDDLE = _get_component_type("FLOWING_PUDDLE_COMPONENT")
    FOCUS = _get_component_type("FOCUS_COMPONENT")
    FOOTPRINT = _get_component_type("FOOTPRINT_COMPONENT")
    GAME = _get_component_type("GAME_COMPONENT")
    GAMEPLAY = _get_component_type("GAMEPLAY_COMPONENT")
    GARDENING = _get_component_type("GARDENING_COMPONENT")
    IDLE = _get_component_type("IDLE_COMPONENT")
    INVENTORY = _get_component_type("INVENTORY_COMPONENT")
    INVENTORY_ITEM = _get_component_type("INVENTORY_ITEM_COMPONENT")
    JEWELRY = _get_component_type("JEWELRY_COMPONENT")
    LIGHTING = _get_component_type("LIGHTING_COMPONENT")
    LINE_OF_SIGHT = _get_component_type("LINE_OF_SIGHT_COMPONENT")
    LINKED_OBJECT = _get_component_type("LINKED_OBJECT_COMPONENT")
    LIVE_DRAG = _get_component_type("LIVE_DRAG_COMPONENT")
    LIVE_DRAG_TARGET = _get_component_type("LIVE_DRAG_TARGET_COMPONENT")
    LUNAR_PHASE_AWARE = _get_component_type("LUNAR_PHASE_AWARE_COMPONENT")
    MANNEQUIN = _get_component_type("MANNEQUIN_COMPONENT")
    MODULAR_OBJECT = _get_component_type("MODULAR_OBJECT_COMPONENT")
    NAME = _get_component_type("NAME_COMPONENT")
    NARRATIVE_AWARE = _get_component_type("NARRATIVE_AWARE_COMPONENT")
    NEW_OBJECT = _get_component_type("NEW_OBJECT_COMPONENT")
    OBJECT_AGE = _get_component_type("OBJECT_AGE_COMPONENT")
    OBJECT_CLAIM = _get_component_type("OBJECT_CLAIM_COMPONENT")
    OBJECT_FASHION_MARKETPLACE = _get_component_type("OBJECT_FASHION_MARKETPLACE_COMPONENT")
    OBJECT_LOCKING = _get_component_type("OBJECT_LOCKING_COMPONENT")
    OBJECT_MARKETPLACE = _get_component_type("OBJECT_MARKETPLACE_COMPONENT")
    OBJECT_RELATIONSHIP = _get_component_type("OBJECT_RELATIONSHIP_COMPONENT")
    OBJECT_ROUTING = _get_component_type("OBJECT_ROUTING_COMPONENT")
    OBJECT_TELEPORTATION = _get_component_type("OBJECT_TELEPORTATION_COMPONENT")
    OWNABLE = _get_component_type("OWNABLE_COMPONENT")
    OWNING_HOUSEOLD = _get_component_type("OWNING_HOUSEOLD_COMPONENT")
    PARENT_TO_SIM_HEAD = _get_component_type("PARENT_TO_SIM_HEAD_COMPONENT")
    PORTAL = _get_component_type("PORTAL_COMPONENT")
    PORTAL_ANIMATION = _get_component_type("PORTAL_ANIMATION_COMPONENT")
    PORTAL_LOCKING = _get_component_type("PORTAL_LOCKING_COMPONENT")
    POSITION = _get_component_type("POSITION_COMPONENT")
    PRIVACY = _get_component_type("PRIVACY_COMPONENT")
    PROCEDURAL_ANIMATION = _get_component_type("PROCEDURAL_ANIMATION_COMPONENT")
    PROXIMITY = _get_component_type("PROXIMITY_COMPONENT")
    RENDER = _get_component_type("RENDER_COMPONENT")
    RETAIL = _get_component_type("RETAIL_COMPONENT")
    ROUTING = _get_component_type("ROUTING_COMPONENT")
    SCHOLARSHIP_LETTER = _get_component_type("SCHOLARSHIP_LETTER_COMPONENT")
    SEASON_AWARE = _get_component_type("SEASON_AWARE_COMPONENT")
    SIM = _get_component_type("SIM_COMPONENT")
    SIM_VISUALIZER = _get_component_type("SIM_VISUALIZER_COMPONENT")
    SITUATION_SCHEDULER = _get_component_type("SITUATION_SCHEDULER_COMPONENT")
    SLOT = _get_component_type("SLOT_COMPONENT")
    SPAWN_POINT = _get_component_type("SPAWN_POINT_COMPONENT")
    SPAWNER = _get_component_type("SPAWNER_COMPONENT")
    STAGE_MARK = _get_component_type("STAGE_MARK_COMPONENT")
    STATE = _get_component_type("STATE_COMPONENT")
    STATISTIC = _get_component_type("STATISTIC_COMPONENT")
    STEREO = _get_component_type("STEREO_COMPONENT")
    STOLEN = _get_component_type("STOLEN_COMPONENT")
    STORED_ACTOR_LOCATION = _get_component_type("STORED_ACTOR_LOCATION_COMPONENT")
    STORED_AUDIO = _get_component_type("STORED_AUDIO_COMPONENT")
    STORED_INFO = _get_component_type("STORED_INFO_COMPONENT")
    STORED_OBJECT_INFO = _get_component_type("STORED_OBJECT_INFO_COMPONENT")
    STORED_SIM_INFO = _get_component_type("STORED_SIM_INFO_COMPONENT")
    TIME_OF_DAY = _get_component_type("TIME_OF_DAY_COMPONENT")
    TOOLTIP = _get_component_type("TOOLTIP_COMPONENT")
    TOPIC = _get_component_type("TOPIC_COMPONENT")
    UTILITIES = _get_component_type("UTILITIES_COMPONENT")
    VEHICLE = _get_component_type("VEHICLE_COMPONENT")
    VIDEO = _get_component_type("VIDEO_COMPONENT")
    WAITING_LINE = _get_component_type("WAITING_LINE_COMPONENT")
    WEATHER_AWARE = _get_component_type("WEATHER_AWARE_COMPONENT")
    WHIM = _get_component_type("WHIM_COMPONENT")
    ZONE_MODIFIER = _get_component_type("ZONE_MODIFIER_COMPONENT")


class OmutsuComponentsService(OmutsuService):

    def has_object_component(self, game_object, component_type):
        if not (component_type is None or isinstance(game_object, ComponentContainer)):
            return False
        return game_object.has_component(component_type)

    def get_object_component(self, game_object, component_type, add_dynamic=False):
        if not (component_type is None or isinstance(game_object, ComponentContainer)):
            return
        if add_dynamic:
            if not game_object.has_component(component_type):
                self.add_dynamic_component(game_object, component_type)
            return game_object.get_component(component_type)

    def add_dynamic_component(self, game_object, component_type):
        if component_type is not None:
            if isinstance(game_object, ComponentContainer):
                if hasattr(game_object, "add_dynamic_component"):
                    game_object.add_dynamic_component(component_type)


_COMPONENTS_SERVICE = OmutsuComponentsService("components")

def get_components_service() -> OmutsuComponentsService:
    return _COMPONENTS_SERVICE
