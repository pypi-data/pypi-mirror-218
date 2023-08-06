import math
from abc import abstractmethod, ABC
from datetime import date


from zmanim.util.geo_location import GeoLocation


class AstronomicalCalculations(ABC):
    GEOMETRIC_ZENITH = 90.0
    REFRACTION = 34.0 / 60.0
    SOLAR_RADIUS = 16 / 60.0
    EARTH_RADIUS = 6356.9  # km

    def __init__(self):
        pass

    def elevation_adjustment(self, elevation: float) -> float:
        return math.degrees(
            math.acos(self.EARTH_RADIUS / (self.EARTH_RADIUS + (elevation / 1000.0)))
        )

    def adjusted_zenith(self, zenith: float, elevation: float) -> float:
        if zenith != self.GEOMETRIC_ZENITH:
            return zenith
        return (
            zenith
            + self.SOLAR_RADIUS
            + self.REFRACTION
            + self.elevation_adjustment(elevation)
        )

    @abstractmethod
    def utc_sunrise(
        self,
        target_date: date,
        geo_location: GeoLocation,
        zenith: float,
        adjust_for_elevation: bool = False,
    ) -> float:
        pass

    @abstractmethod
    def utc_sunset(
        self,
        target_date: date,
        geo_location: GeoLocation,
        zenith: float,
        adjust_for_elevation: bool = False,
    ) -> float:
        pass
