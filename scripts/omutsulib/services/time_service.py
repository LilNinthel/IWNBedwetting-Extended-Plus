from collections import namedtuple
import date_and_time, services
from omutsulib.services.service import OmutsuService

class OmutsuClockSpeedMode:
    PAUSED = 0
    NORMAL = 1
    SPEED2 = 2
    SPEED3 = 3
    INTERACTION_STARTUP_SPEED = 4
    SUPER_SPEED3 = 5


class OmutsuDay:
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


ALL_DAYS = (
 OmutsuDay.SUNDAY, OmutsuDay.MONDAY, OmutsuDay.TUESDAY, OmutsuDay.WEDNESDAY, OmutsuDay.THURSDAY, OmutsuDay.FRIDAY, OmutsuDay.SATURDAY)
_WeekSchedule = namedtuple("_WeekSchedule", ('days', 'start_hour', 'start_minute',
                                             'end_hour', 'end_minute'))

def WeekSchedule(days=ALL_DAYS, start_hour=12, start_minute=0, end_hour=None, end_minute=60):
    return _WeekSchedule(days, start_hour, start_minute, end_hour, end_minute)


class OmutsuTimeService(OmutsuService):
    TICKS_PER_REAL_WORLD_SECOND = date_and_time.TICKS_PER_REAL_WORLD_SECOND
    REAL_MILLISECONDS_PER_SIM_SECOND = date_and_time.REAL_MILLISECONDS_PER_SIM_SECOND
    MILLISECONDS_PER_SECOND = date_and_time.MILLISECONDS_PER_SECOND
    SECONDS_PER_MINUTE = date_and_time.SECONDS_PER_MINUTE
    MINUTES_PER_HOUR = date_and_time.MINUTES_PER_HOUR
    HOURS_PER_DAY = date_and_time.HOURS_PER_DAY
    DAYS_PER_WEEK = date_and_time.DAYS_PER_WEEK
    SECONDS_PER_HOUR = SECONDS_PER_MINUTE * MINUTES_PER_HOUR
    SECONDS_PER_DAY = SECONDS_PER_HOUR * HOURS_PER_DAY
    SECONDS_PER_WEEK = SECONDS_PER_DAY * DAYS_PER_WEEK

    def get_current_clock_speed(self):
        return services.game_clock_service().clock_speed

    def get_current_clock_speed_scale(self):
        return services.game_clock_service().current_clock_speed_scale()

    def set_current_clock_speed(self, speed_mode):
        return services.game_clock_service().set_clock_speed(speed_mode)

    def is_day_time(self):
        return services.time_service().is_day_time()

    def is_night_time(self):
        return not services.time_service().is_day_time()

    def get_absolute_ticks(self):
        return services.time_service().sim_now.absolute_ticks()

    def get_second_of_minute(self):
        return services.time_service().sim_now.second()

    def get_minute_of_hour(self):
        return services.time_service().sim_now.minute()

    def get_hour_of_day(self):
        return services.time_service().sim_now.hour()

    def get_day_of_week(self):
        return services.time_service().sim_now.day()

    def get_absolute_seconds(self):
        return int(services.time_service().sim_now.absolute_seconds())

    def get_absolute_minutes(self):
        return int(services.time_service().sim_now.absolute_minutes())

    def get_absolute_hours(self):
        return int(services.time_service().sim_now.absolute_hours())

    def get_absolute_days(self):
        return int(services.time_service().sim_now.absolute_days())

    def get_absolute_weeks(self):
        return services.time_service().sim_now.week()

    def repr_ticks(self, ticks):
        absolute_seconds = ticks / self.REAL_MILLISECONDS_PER_SIM_SECOND
        return "{0:02}:{1:02}:{2:02} day:{3} week:{4}".format(int(absolute_seconds / self.SECONDS_PER_HOUR % self.HOURS_PER_DAY), int(absolute_seconds / self.SECONDS_PER_MINUTE % self.MINUTES_PER_HOUR), int(absolute_seconds % self.SECONDS_PER_MINUTE), int(absolute_seconds / self.SECONDS_PER_DAY % self.DAYS_PER_WEEK), int(absolute_seconds / self.SECONDS_PER_WEEK))


_TIME_SERVICE = OmutsuTimeService("time")

def get_time_service() -> OmutsuTimeService:
    return _TIME_SERVICE