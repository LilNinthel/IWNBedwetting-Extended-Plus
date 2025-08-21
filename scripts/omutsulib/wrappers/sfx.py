import sims4.hash_util
from audio.primitive import PlaySound
from omutsulib.wrappers.wrappers_manager import OmutsuInstance


class _SuperOmutsuSFX(OmutsuInstance):

    def __init__(self, game_object, sound_name, immediate=True, **kwargs):
        super().__init__(None)
        self._sound = PlaySound(game_object, sims4.hash_util.hash64(sound_name), immediate=immediate, **kwargs)

    def play(self):
        self._sound.start()

    def stop(self):
        self._sound.stop()


class OmutsuSFX(_SuperOmutsuSFX):

    def __init__(self, game_object, sound_name, immediate=True, **kwargs):
        (super().__init__)(game_object, sound_name, immediate=immediate, **kwargs)
