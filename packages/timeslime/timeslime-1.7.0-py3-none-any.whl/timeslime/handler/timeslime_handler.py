"""timeslime handler class"""
from ast import literal_eval
from datetime import date, datetime, timedelta, timezone
from typing import Optional

from peewee import DoesNotExist
from requests.exceptions import ConnectionError as RequestConnectionError

from timeslime.handler import (
    DatabaseHandler,
    NtpServerHandler,
    SettingsHandler,
    StateHandler,
    TimeslimeServerHandler,
)
from timeslime.models import Timespan


class TimeslimeHandler():
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        settings_handler: SettingsHandler,
        database_handler: DatabaseHandler,
        ntp_server_handler: NtpServerHandler,
        state_handler: StateHandler = None,
        timeslime_server_handler: TimeslimeServerHandler = None,
        today: Optional[datetime] = None,
    ):
        """initialize timeslime handler
        :param today: just for testing"""
        self.settings_handler = settings_handler
        self.database_handler = database_handler
        self.ntp_server_handler = ntp_server_handler
        self.state_handler = state_handler
        self.timeslime_server_handler = timeslime_server_handler
        self.on_start = None
        self.on_stop = None
        self.today = today

        if self.settings_handler:
            self.settings_handler.sync()
            self._set_daily_working_time(self.settings_handler, date.today().weekday())
            self._set_timeslime_server_handler(self.settings_handler)
            self.sync()

        self.timespan = self.database_handler.get_recent_timespan()

    def _set_daily_working_time(self, settings_handler: SettingsHandler, weekday: int):
        if not settings_handler.contains('weekly_hours'):
            print('Please run `timeslime init` to configure timeslime')
            raise KeyError

        weekly_hours = literal_eval(settings_handler.get('weekly_hours').value)
        daily_working_time_array = weekly_hours[weekday].split(':')
        self._daily_working_time = timedelta(hours=int(daily_working_time_array[0]), minutes=int(daily_working_time_array[1]), seconds=int(daily_working_time_array[2]))

    def _set_timeslime_server_handler(self, settings_handler: SettingsHandler):
        if self.timeslime_server_handler is not None:
            return

        if (
            settings_handler.contains("timeslime_server")
            and settings_handler.contains("username")
            and settings_handler.contains("password")
        ):
            timeslime_server = settings_handler.get("timeslime_server")
            username = settings_handler.get("username")
            password = settings_handler.get("password")
            self.timeslime_server_handler = TimeslimeServerHandler(
                timeslime_server.value, username.value, password.value
            )
        else:
            self.timeslime_server_handler = None

    def start_time(self, start_time_str: str = "") -> datetime:
        """start time at current system time or at `start_time_str`
        :param start_time_str: start time must be a valid time (e.g.: 8:00)"""
        current_time = self.__get_time(start_time_str)
        self.stop_time()
        self.timespan = Timespan()
        self.timespan.start_time = current_time
        self.timespan = self.database_handler.save_timespan(self.timespan)
        if self.timeslime_server_handler is not None:
            try:
                self.timeslime_server_handler.send_timespan(self.timespan)
            except RequestConnectionError:
                pass
        if self.on_start is not None:
            self.on_start()

        return self.timespan.start_time

    def stop_time(self, stop_time_str: str = "") -> Optional[datetime]:
        """stop time at current system time or at `stop_time_str`
        :param stop_time_str: stop time must be a valid time (e.g.: 8:00)"""
        current_time = self.__get_time(stop_time_str)
        if self.timespan is not None and self.timespan.start_time is not None and self.timespan.stop_time is None:
            self.timespan.stop_time = current_time
            self.timespan = self.database_handler.save_timespan(self.timespan)
            if self.timeslime_server_handler is not None:
                try:
                    self.timeslime_server_handler.send_timespan(self.timespan)
                except RequestConnectionError:
                    pass
        if self.on_stop is not None:
            self.on_stop()

        if self.timespan:
            return self.timespan.stop_time

        return None

    def __get_time(self, time_str: str = ""):
        """get time"""
        if time_str:
            if not self.today:
                now = datetime.now()
            else:
                now = self.today
            try:
                requested_time = datetime.strptime(time_str, "%H:%M")
            except ValueError as value_error:
                raise ValueError(
                    "Time must be in the format HH:mm (eg. 8:00)!"
                ) from value_error
            time = now.replace(
                hour=requested_time.hour,
                minute=requested_time.minute,
                second=0,
                microsecond=0,
            )
            time = time.astimezone(timezone.utc)
        elif not self.ntp_server_handler.ntp_server_is_synchronized:
            raise ValueError(
                "NTP server is not synchronized yet. "
                "Wait a few seconds to get an accurate time tracking."
            )
        else:
            time = datetime.now(tz=timezone.utc)

        return time

    def get_elapsed_time(self, datetime_now: Optional[datetime] = None) -> bool:
        if not self.ntp_server_handler.ntp_server_is_synchronized:
            print('NTP server is not synchronized yet. Wait a few seconds to get an accurate time tracking.')
            return
        if not datetime_now:
            datetime_now = datetime.now()

        daily_sum_in_seconds = self.database_handler.get_tracked_time_in_seconds(
            datetime_now
        )
        current_timedelta = timedelta(seconds=0)
        if self.timespan is not None and self.timespan.stop_time is None:
            current_timedelta = datetime.now(tz=timezone.utc) - self.timespan.start_time
        return self._daily_working_time - daily_sum_in_seconds - current_timedelta

    def is_running(self):
        if self.database_handler.get_recent_timespan() is not None:
            return True
        else:
            return False

    def get(self, guid: str) -> Timespan:
        """get a timespan
        : param guid: defines guid"""
        return self.database_handler.read_timespan(guid)

    def get_all(
        self,
        start_time: Optional[datetime] = None,
        update_at: Optional[datetime] = None,
    ) -> list[Timespan]:
        """get all timespans
        :param filter_date: defines date"""
        return self.database_handler.read_timespans(
            start_time=start_time, update_at=update_at
        )

    def contains(self, guid: str) -> bool:
        """check if list contains defined id
        :param guid: defines guid"""
        try:
            self.database_handler.read_timespan(guid)
            return True
        except DoesNotExist:
            return False

    def sync(self, ignore_state: bool = False) -> None:
        """sync timespans with a timeslime server
        :param ignore_state: define to ignore the state (everything will be synchronized)"""
        if self.timeslime_server_handler is not None:
            last_timespan_sync = None
            if not ignore_state and self.state_handler:
                last_timespan_sync = self.state_handler.get_state().last_timespan_sync

            timespans_response = self.timeslime_server_handler.get_timespans(
                last_timespan_sync
            )

            for timespan in timespans_response.timespans:
                if not self.contains(timespan.id):
                    self.database_handler.save_timespan(timespan)
                else:
                    local_timespan = self.get(timespan.id)
                    if local_timespan.updated_at.tzinfo is None:
                        local_timespan.updated_at = local_timespan.updated_at.replace(
                            tzinfo=timezone.utc
                        )
                    if timespan.updated_at.tzinfo is None:
                        timespan.updated_at = timespan.updated_at.replace(
                            tzinfo=timezone.utc
                        )
                    if local_timespan.updated_at < timespan.updated_at:
                        self.database_handler.save_timespan(timespan)

            self.timeslime_server_handler.send_timespan_list(
                self.get_all(last_timespan_sync)
            )

            if self.state_handler:
                self.state_handler.set_last_timespan_sync(
                    timespans_response.request_time
                )
