from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class UnitsTemperature(Enum):
    """
    The units used to represent a temperature.

    Properties
    ----------
    CELSIUS: degree Celsius unit.
    FAHRENHEIT: degree Fahrenheit unit.
    KELVIN: Kelvin unit.
    RANKINE: degree Rankine unit.
    """

    CELSIUS = "°C"
    FAHRENHEIT = "°F"
    KELVIN = "K"
    RANKINE = "°R"
