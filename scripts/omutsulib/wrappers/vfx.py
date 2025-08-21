import alarms, sims4.hash_util, vfx
from date_and_time import TimeSpan
from omutsulib.wrappers.wrappers_manager import OmutsuInstance


class _SuperOmutsuVFX(OmutsuInstance):

    def __init__(self, game_object, effect_name, joint_name_or_hash, delay_ticks=0, expire_ticks=0, **kwargs):
        super().__init__(None)
        joint_name_hash = sims4.hash_util.hash32(joint_name_or_hash) if isinstance(joint_name_or_hash, str) else joint_name_or_hash
        self._effect = vfx.PlayEffect(game_object, effect_name=effect_name, joint_name=joint_name_hash, **kwargs)
        self._delay_ticks = delay_ticks
        self._delay_alarm = None
        self._expire_ticks = expire_ticks
        self._expire_alarm = None

    def play_with_delay(self):
        if self._delay_alarm is None:
            if self._delay_ticks <= 0:
                raise ValueError("No delay ticks were provided.")
            self._delay_alarm = alarms.add_alarm(self, TimeSpan(self._delay_ticks), self.play)

    def play(self, one_shot=False):
        if self._effect is not None:
            if one_shot:
                self._effect.start_one_shot()
            else:
                self._effect.start()
            self._delay_alarm = None
            if self._expire_ticks > 0:
                self._expire_alarm = alarms.add_alarm(self, TimeSpan(self._expire_ticks), self.stop)

    def stop(self, immediate=False):
        if self._effect is not None:
            self._effect.stop(immediate=immediate)
            self._effect = None
            self._delay_alarm = None
            self._expire_alarm = None


class OmutsuVFX(_SuperOmutsuVFX):

    def __init__(self, game_object, effect_name, joint_name, **kwargs):
        super().__init__(game_object, effect_name, joint_name, **kwargs)
