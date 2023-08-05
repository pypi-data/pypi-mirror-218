from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class UnitsPower(Enum):
    """
    The units used to represent power.

    Properties
    ----------
    YOTTAWATT: yottawatt unit.
    ZETTAWATT: zettawatt unit.
    EXAWATT: exawatt unit.
    PETAWATT: petawatt unit.
    TERAWATT: terawatt unit.
    GIGAWATT: gigawatt unit.
    MEGAWATT: megawatt unit.
    KILOWATT: kilowatt unit.
    HECTOWATT: hectowatt unit.
    DECAWATT: decawatt unit.
    WATT: watt unit.
    DECIWATT: deciwatt unit.
    CENTIWATT: centiwatt unit.
    MILLIWATT: milliwatt unit.
    MICROWATT: microwatt unit.
    NANOWATT: nanowatt unit.
    PICOWATT: picowatt unit.
    FEMTOWATT: femtowatt unit.
    ATTOWATT: attowatt unit.
    ZEPTOWATT: zeptowatt unit.
    YOCTOWATT: yoctowatt unit.
    """

    YOTTAWATT = "YW"
    ZETTAWATT = "ZW"
    EXAWATT = "EW"
    PETAWATT = "PW"
    TERAWATT = "TW"
    GIGAWATT = "GW"
    MEGAWATT = "MW"
    KILOWATT = "kW"
    HECTOWATT = "hW"
    DECAWATT = "daW"
    WATT = "W"
    DECIWATT = "dW"
    CENTIWATT = "cW"
    MILLIWATT = "mW"
    MICROWATT = "µW"
    NANOWATT = "nW"
    PICOWATT = "pW"
    FEMTOWATT = "fW"
    ATTOWATT = "aW"
    ZEPTOWATT = "zW"
    YOCTOWATT = "yW"
