import enum


class DiaperWetness(enum.Int, export=False):
    DRY = 0,
    BARELY_WET = 1,
    WET = 2,
    VERY_WET = 3,
    SOAKED = 4,
    LEAKING = 5,
    OVERFLOWING = 6


class DiaperMessiness(enum.Int, export=False):
    CLEAN = 0,
    BARELY_MESSY = 1,
    MESSY = 2,
    VERY_MESSY = 3,
    HYPER_MESS = 4
