from buffs.buff import Buff
from interactions.social.social_mixer_interaction import SocialMixerInteraction
from objects.doors.door import Door
from objects.game_object import GameObject
from objects.pools.ocean import Ocean
from objects.pools.pool import SwimmingPool
from objects.pools.pool_seat import PoolSeat
from objects.script_object import ScriptObject
from objects.terrain import Terrain
from sims.self_interactions import NPCLeaveLotInteraction
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4.math import Location
from omutsulib.wrappers.game_object.game_object import OmutsuGameObject
from omutsulib.wrappers.sim.sim import OmutsuSim
from world.lot import Lot
is_sim = lambda obj: isinstance(obj, SimInfo) or isinstance(obj, Sim)
is_sim_instance = lambda obj: isinstance(obj, Sim)
is_sim_info = lambda obj: isinstance(obj, SimInfo)
is_omutsu_sim = lambda obj: isinstance(obj, OmutsuSim)
is_script_object = lambda obj: isinstance(obj, ScriptObject)
is_game_object = lambda obj: isinstance(obj, GameObject)
is_terrain = lambda obj: isinstance(obj, Terrain)
is_ocean = lambda obj: isinstance(obj, Ocean)
is_swimming_pool = lambda obj: isinstance(obj, SwimmingPool)
is_pool_seat = lambda obj: isinstance(obj, PoolSeat)
is_door_object = lambda obj: isinstance(obj, Door)
is_omutsu_game_object = lambda obj: isinstance(obj, OmutsuGameObject)
is_buff = lambda obj: isinstance(obj, Buff)
is_location = lambda obj: isinstance(obj, Location)
is_lot = lambda obj: isinstance(obj, Lot)
is_social_mixer_interaction = lambda obj: isinstance(obj, SocialMixerInteraction)
is_npc_leave_lot_interaction = lambda obj: isinstance(obj, NPCLeaveLotInteraction)
has_routing_component = lambda obj: getattr(obj, "routing_component", None) is not None
