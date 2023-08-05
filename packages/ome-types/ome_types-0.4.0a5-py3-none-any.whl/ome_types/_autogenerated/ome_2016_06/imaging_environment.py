from typing import Optional

from pydantic import Field

from ome_types._autogenerated.ome_2016_06.map import Map
from ome_types._autogenerated.ome_2016_06.units_pressure import UnitsPressure
from ome_types._autogenerated.ome_2016_06.units_temperature import UnitsTemperature
from ome_types._mixins._base_type import OMEType

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class ImagingEnvironment(OMEType):
    """
    This describes the environment that the biological sample was in during the
    experiment.

    Parameters
    ----------
    map:
    temperature: The Temperature is the define units.
    temperature_unit: The units the Temperature is in -
        default:Celsius[°C].
    air_pressure: AirPressure is the define units.
    air_pressure_unit: The units the AirPressure is in -
        default:millibars[mbar].
    humidity: Humidity around the sample [units:none] A fraction, as a
        value from 0.0 to 1.0.
    co2_percent: Carbon Dioxide concentration around the sample
        [units:none] A fraction, as a value from 0.0 to 1.0.
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    map: Optional[Map] = Field(
        default=None,
        metadata={
            "name": "Map",
            "type": "Element",
        }
    )
    temperature: Optional[float] = Field(
        default=None,
        metadata={
            "name": "Temperature",
            "type": "Attribute",
        }
    )
    temperature_unit: UnitsTemperature = Field(
        default=UnitsTemperature.CELSIUS,
        metadata={
            "name": "TemperatureUnit",
            "type": "Attribute",
        }
    )
    air_pressure: Optional[float] = Field(
        default=None,
        metadata={
            "name": "AirPressure",
            "type": "Attribute",
        }
    )
    air_pressure_unit: UnitsPressure = Field(
        default=UnitsPressure.MILLIBAR,
        metadata={
            "name": "AirPressureUnit",
            "type": "Attribute",
        }
    )
    humidity: Optional[float] = Field(
        default=None,
        metadata={
            "name": "Humidity",
            "type": "Attribute",
            "min_inclusive": 0.0,
            "max_inclusive": 1.0,
        },
        ge=0.0,
        le=1.0
    )
    co2_percent: Optional[float] = Field(
        default=None,
        metadata={
            "name": "CO2Percent",
            "type": "Attribute",
            "min_inclusive": 0.0,
            "max_inclusive": 1.0,
        },
        ge=0.0,
        le=1.0
    )
