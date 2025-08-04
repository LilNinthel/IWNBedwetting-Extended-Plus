from reservation.reservation_result import ReservationResult
from omutsulib.wrappers.game_object.super_game_object import _SuperOmutsuGameObject

class _OmutsuObjectReservationMixin(_SuperOmutsuGameObject):

    def is_in_use(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            return hasattr(object_instance, "self_or_part_in_use") and object_instance.self_or_part_in_use
        return False

    def is_in_use_by(self, sim_identifier):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            omutsu_sim = OmutsuSim(sim_identifier)
            if omutsu_sim is not None:
                return hasattr(object_instance, "in_use_by") and object_instance.in_use_by(omutsu_sim.get_sim_instance())
            return False

    def get_reservations_omutsu_sims(self):
        object_instance = self.get_object_instance()
        if object_instance is not None:
            from omutsulib.wrappers.sim.sim import OmutsuSim
            return tuple((OmutsuSim(sim_identifier) for sim_identifier in hasattr(object_instance, "get_users") and object_instance.get_users(sims_only=True)))
        return ()

    @classmethod
    def begin_reservation(cls, handler):
        try:
            return handler.begin_reservation()
        except:
            return ReservationResult(False)

    @classmethod
    def end_reservation(cls, handler):
        try:
            return handler.end_reservation()
        except:
            return ReservationResult(False)

    def get_reservation_handler(self, omutsu_sim, *args, **kwargs):
        if omutsu_sim is not None:
            sim_instance = omutsu_sim.get_sim_instance()
            if sim_instance is not None:
                object_instance = self.get_object_instance()
                if object_instance is not None:
                    while object_instance.parent is not None:
                        parent = object_instance.parent
                        if parent is not None:
                            object_instance = parent
                        else:
                            break

                    if hasattr(object_instance, "get_reservation_handler"):
                        return (object_instance.get_reservation_handler)(sim_instance, *args, **kwargs)
