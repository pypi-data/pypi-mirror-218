from datetime import date, datetime, timedelta
from typing import Optional

from dateutil import tz

from zmanim.util.astronomical_calculations import AstronomicalCalculations
from zmanim.util.geo_location import GeoLocation
from zmanim.util.math_helper import MathHelper
from zmanim.util.noaa_calculator import NOAACalculator
from zmanim.exceptions.artic_circle import ArticCircleException


class AstronomicalCalendar(MathHelper):
    """
    The base model that contains all the astronomical calculations.
    This class is used by the ZmanimCalendar
    """

    GEOMETRIC_ZENITH = 90
    CIVIL_ZENITH = 96
    NAUTICAL_ZENITH = 102
    ASTRONOMICAL_ZENITH = 108

    def __init__(
        self,
        geo_location: Optional[GeoLocation] = None,
        date: Optional[date] = None,
        calculator: Optional[AstronomicalCalculations] = None,
    ):
        """
        Create an AstronomicalCalendar object with the required parameters.

        Args:
            geo_location (Optional[GeoLocation], optional): The location to provide Zmanim for. Defaults to GeoLocation.GMT().
            date (Optional[date], optional): The date to get Zmanim for. Defaults to datetime.today().
            calculator (Optional[AstronomicalCalculations], optional): _description_. Defaults to None.
        """
        if geo_location is None:
            geo_location = GeoLocation.GMT()
        if date is None:
            date = datetime.today()
        if calculator is None:
            calculator = NOAACalculator()
        self.geo_location = geo_location
        self.date = date
        self.astronomical_calculator = calculator

    def __repr__(self):
        return "%s(geo_location=%r, date=%r, calculator=%r)" % (
            self.__module__ + "." + self.__class__.__qualname__,
            self.geo_location,
            self.date,
            self.astronomical_calculator,
        )

    def sunrise(self) -> datetime:
        return self._date_time_from_time_of_day(
            self.utc_sunrise(self.GEOMETRIC_ZENITH), "sunrise"
        )

    def sea_level_sunrise(self) -> datetime:
        return self.sunrise_offset_by_degrees(self.GEOMETRIC_ZENITH)

    def sunrise_offset_by_degrees(self, offset_zenith: float) -> datetime:
        return self._date_time_from_time_of_day(
            self.utc_sea_level_sunrise(offset_zenith), "sunrise"
        )

    def sunset(self) -> datetime:
        return self._date_time_from_time_of_day(
            self.utc_sunset(self.GEOMETRIC_ZENITH), "sunset"
        )

    def sea_level_sunset(self) -> datetime:
        return self.sunset_offset_by_degrees(self.GEOMETRIC_ZENITH)

    def sunset_offset_by_degrees(self, offset_zenith: float) -> datetime:
        return self._date_time_from_time_of_day(
            self.utc_sea_level_sunset(offset_zenith), "sunset"
        )

    def utc_sunrise(self, zenith: float) -> float:
        return self.astronomical_calculator.utc_sunrise(
            self._adjusted_date(), self.geo_location, zenith, adjust_for_elevation=True
        )

    def utc_sea_level_sunrise(self, zenith: float) -> float:
        return self.astronomical_calculator.utc_sunrise(
            self._adjusted_date(), self.geo_location, zenith, adjust_for_elevation=False
        )

    def utc_sunset(self, zenith: float) -> float:
        return self.astronomical_calculator.utc_sunset(
            self._adjusted_date(), self.geo_location, zenith, adjust_for_elevation=True
        )

    def utc_sea_level_sunset(self, zenith: float) -> float:
        return self.astronomical_calculator.utc_sunset(
            self._adjusted_date(), self.geo_location, zenith, adjust_for_elevation=False
        )

    def temporal_hour(
        self,
        sunrise: Optional[datetime] = None,
        sunset: Optional[datetime] = None,
    ) -> float:
        sunrise = self.sea_level_sunrise()
        sunset = self.sea_level_sunset()

        if sunset is None or sunrise is None:
            raise ArticCircleException()

        daytime_hours = float((sunset - sunrise).total_seconds() / 3600.0)
        return (daytime_hours / 12) * self.HOUR_MILLIS

    def sun_transit(self) -> datetime:
        sunrise = self.sea_level_sunrise()
        sunset = self.sea_level_sunset()
        noon_hour = (self.temporal_hour(sunrise, sunset) / self.HOUR_MILLIS) * 6.0
        return sunrise + timedelta(noon_hour / 24.0)

    def _date_time_from_time_of_day(
        self, time_of_day: float, mode: str
    ) -> datetime:

        hours, remainder = divmod(time_of_day * 3600, 3600)
        minutes, remainder = divmod(remainder, 60)
        seconds, microseconds = divmod(remainder * 10**6, 10**6)
        adjusted_date = self._adjusted_date()
        year, month, day = adjusted_date.year, adjusted_date.month, adjusted_date.day
        utc_time = datetime(
            year,
            month,
            day,
            int(hours),
            int(minutes),
            int(seconds),
            int(microseconds),
            tzinfo=tz.tzutc(),
        )

        # adjust date if utc time reflects a wraparound from the local offset
        local_offset = (
            self.geo_location.local_mean_time_offset()
            + self.geo_location.standard_time_offset()
        ) / self.HOUR_MILLIS
        if (
            hours + local_offset > 18 and mode == "sunrise"
        ):  # sunrise after 6pm indicates the UTC date has occurred earlier
            utc_time -= timedelta(1)
        elif (
            hours + local_offset < 6 and mode == "sunset"
        ):  # sunset before 6am indicates the UTC date has occurred later
            utc_time += timedelta(1)

        return self._convert_date_time_for_zone(utc_time)

    def _adjusted_date(self) -> date:
        return self.date + timedelta(days=self.geo_location.antimeridian_adjustment())

    def _convert_date_time_for_zone(self, utc_time: datetime) -> datetime:
        return utc_time.astimezone(self.geo_location.time_zone)
