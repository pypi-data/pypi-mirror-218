from datetime import datetime, timedelta, date
from typing import Optional

from zmanim.astronomical_calendar import AstronomicalCalendar
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar
from zmanim.astronomical_calendar import AstronomicalCalendar
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar
from zmanim.util.astronomical_calculations import AstronomicalCalculations
from zmanim.util.geo_location import GeoLocation


class ZmanimCalendar(AstronomicalCalendar):
    def __init__(
        self,
        candle_lighting_offset: int = 18,
        geo_location: Optional[GeoLocation] = None,
        date: Optional[date] = None,
        calculator: Optional[AstronomicalCalculations] = None,
    ):
        """The main Zmanim calendar class that contains all the Zmanim and calendar calculations.

        Args:
            candle_lighting_offset (Optional[int], optional): How many minutes before sunset is Candle Lighting. Defaults to 18.
            geo_location (Optional[GeoLocation], optional): The location to provide Zmanim for. Defaults to GeoLocation.GMT().
            date (Optional[date], optional): The date to get Zmanim for. Defaults to datetime.today().
            calculator (Optional[AstronomicalCalculations], optional): _description_. Defaults to None.
        """
        super(ZmanimCalendar, self).__init__(geo_location, date, calculator)
        self.candle_lighting_offset = candle_lighting_offset
        self.use_elevation = False

    def __repr__(self):
        return (
            "%s(candle_lighting_offset=%r, geo_location=%r, date=%r, calculator=%r)"
            % (
                self.__module__ + "." + self.__class__.__qualname__,
                self.candle_lighting_offset,
                self.geo_location,
                self.date,
                self.astronomical_calculator,
            )
        )

    def elevation_adjusted_sunrise(self) -> datetime:
        return self.sunrise() if self.use_elevation else self.sea_level_sunrise()

    def hanetz(self) -> datetime:
        return self.elevation_adjusted_sunrise()

    def elevation_adjusted_sunset(self) -> datetime:
        return self.sunset() if self.use_elevation else self.sea_level_sunset()

    def shkia(self) -> datetime:
        return self.elevation_adjusted_sunset()

    def tzais(self, opts: dict = {'degrees': 8.5}) -> datetime:
        degrees, offset, zmanis_offset = self._extract_degrees_offset(opts)
        sunset_for_degrees = self.elevation_adjusted_sunset() if degrees == 0 else self.sunset_offset_by_degrees(self.GEOMETRIC_ZENITH + degrees)
        if zmanis_offset != 0:
            return self._offset_by_minutes_zmanis(sunset_for_degrees, zmanis_offset)
        else:
            return self._offset_by_minutes(sunset_for_degrees, offset)

    def tzais_72(self) -> datetime:
        return self.tzais({'offset': 72})

    def alos(self, opts: dict = {'degrees': 16.1}) -> datetime:
        degrees, offset, zmanis_offset = self._extract_degrees_offset(opts)
        sunrise_for_degrees = self.elevation_adjusted_sunrise() if degrees == 0 else self.sunrise_offset_by_degrees(self.GEOMETRIC_ZENITH + degrees)
        if zmanis_offset != 0:
            return self._offset_by_minutes_zmanis(sunrise_for_degrees, -zmanis_offset)
        else:
            return self._offset_by_minutes(sunrise_for_degrees, -offset)

    def alos_72(self) -> datetime:
        return self.alos({'offset': 72})

    def chatzos(self) -> datetime:
        return self.sun_transit()

    def candle_lighting(self) -> datetime:
        return self._offset_by_minutes(self.sea_level_sunset(), -self.candle_lighting_offset)

    def sof_zman_shma(self, day_start: datetime, day_end: datetime) -> datetime:
        return self._shaos_into_day(day_start, day_end, 3)

    def sof_zman_shma_gra(self) -> datetime:
        return self.sof_zman_shma(self.elevation_adjusted_sunrise(), self.elevation_adjusted_sunset())

    def sof_zman_shma_mga(self) -> datetime:
        return self.sof_zman_shma(self.alos_72(), self.tzais_72())

    def sof_zman_tfila(self, day_start: datetime, day_end: datetime) -> datetime:
        return self._shaos_into_day(day_start, day_end, 4)

    def sof_zman_tfila_gra(self) -> datetime:
        return self.sof_zman_tfila(self.elevation_adjusted_sunrise(), self.elevation_adjusted_sunset())

    def sof_zman_tfila_mga(self) -> datetime:
        return self.sof_zman_tfila(self.alos_72(), self.tzais_72())

    def mincha_gedola(self, day_start: Optional[datetime] = None, day_end: Optional[datetime] = None) -> datetime:
        if day_start is None:
            day_start = self.elevation_adjusted_sunrise()
        if day_end is None:
            day_end = self.elevation_adjusted_sunset()

        return self._shaos_into_day(day_start, day_end, 6.5)

    def mincha_ketana(self, day_start: Optional[datetime] = None, day_end: Optional[datetime] = None) -> datetime:
        if day_start is None:
            day_start = self.elevation_adjusted_sunrise()
        if day_end is None:
            day_end = self.elevation_adjusted_sunset()

        return self._shaos_into_day(day_start, day_end, 9.5)

    def plag_hamincha(self, day_start: Optional[datetime] = None, day_end: Optional[datetime] = None) -> datetime:
        if day_start is None:
            day_start = self.elevation_adjusted_sunrise()
        if day_end is None:
            day_end = self.elevation_adjusted_sunset()

        return self._shaos_into_day(day_start, day_end, 10.75)

    def shaah_zmanis(self, day_start: Optional[datetime], day_end: Optional[datetime]) -> float:
        return self.temporal_hour(day_start, day_end)

    def shaah_zmanis_gra(self) -> float:
        return self.shaah_zmanis(self.elevation_adjusted_sunrise(), self.elevation_adjusted_sunset())

    def shaah_zmanis_mga(self) -> float:
        return self.shaah_zmanis(self.alos_72(), self.tzais_72())

    def shaah_zmanis_by_degrees_and_offset(self, degrees: float, offset: float) -> float:
        opts = {'degrees': degrees, 'offset': offset}
        return self.shaah_zmanis(self.alos(opts), self.tzais(opts))

    def is_assur_bemelacha(self, current_time: datetime, tzais=None, in_israel: Optional[bool]=False):
        if tzais is None:
            tzais_time = self.tzais()
        elif isinstance(tzais, dict):
            tzais_time = self.tzais(tzais)
        else:
            tzais_time = tzais
        jewish_calendar = JewishCalendar(current_time.date())
        jewish_calendar.in_israel = in_israel
        return (current_time <= tzais_time and jewish_calendar.is_assur_bemelacha()) or \
               (current_time >= self.elevation_adjusted_sunset() and jewish_calendar.is_tomorrow_assur_bemelacha())

    def _shaos_into_day(self, day_start: datetime, day_end: datetime, shaos: float) -> datetime:
        shaah_zmanis = self.temporal_hour(day_start, day_end)
        return self._offset_by_minutes(day_start, (shaah_zmanis / self.MINUTE_MILLIS) * shaos)

    def _extract_degrees_offset(self, opts: dict) -> tuple:
        degrees = opts['degrees'] if 'degrees' in opts else 0
        offset = opts['offset'] if 'offset' in opts else 0
        zmanis_offset = opts['zmanis_offset'] if 'zmanis_offset' in opts else 0
        return degrees, offset, zmanis_offset

    def _offset_by_minutes(self, time: datetime, minutes: float) -> datetime:
        return time + timedelta(minutes=minutes)

    def _offset_by_minutes_zmanis(self, time: datetime, minutes: float) -> datetime:
        shaah_zmanis_skew = self.shaah_zmanis_gra() / self.HOUR_MILLIS
        return time + timedelta(minutes=minutes*shaah_zmanis_skew)
