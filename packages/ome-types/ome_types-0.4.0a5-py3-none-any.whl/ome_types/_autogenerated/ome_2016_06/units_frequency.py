from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class UnitsFrequency(Enum):
    """
    The units used to represent frequency.

    Properties
    ----------
    YOTTAHERTZ: yottahertz unit.
    ZETTAHERTZ: zettahertz unit.
    EXAHERTZ: exahertz unit.
    PETAHERTZ: petahertz unit.
    TERAHERTZ: terahertz unit.
    GIGAHERTZ: gigahertz unit.
    MEGAHERTZ: megahertz unit.
    KILOHERTZ: kilohertz unit.
    HECTOHERTZ: hectohertz unit.
    DECAHERTZ: decahertz unit.
    HERTZ: hertz unit.
    DECIHERTZ: decihertz unit.
    CENTIHERTZ: centihertz unit.
    MILLIHERTZ: millihertz unit.
    MICROHERTZ: microhertz unit.
    NANOHERTZ: nanohertz unit.
    PICOHERTZ: picohertz unit.
    FEMTOHERTZ: femtohertz unit.
    ATTOHERTZ: attohertz unit.
    ZEPTOHERTZ: zeptohertz unit.
    YOCTOHERTZ: yoctohertz unit.
    """

    YOTTAHERTZ = "YHz"
    ZETTAHERTZ = "ZHz"
    EXAHERTZ = "EHz"
    PETAHERTZ = "PHz"
    TERAHERTZ = "THz"
    GIGAHERTZ = "GHz"
    MEGAHERTZ = "MHz"
    KILOHERTZ = "kHz"
    HECTOHERTZ = "hHz"
    DECAHERTZ = "daHz"
    HERTZ = "Hz"
    DECIHERTZ = "dHz"
    CENTIHERTZ = "cHz"
    MILLIHERTZ = "mHz"
    MICROHERTZ = "µHz"
    NANOHERTZ = "nHz"
    PICOHERTZ = "pHz"
    FEMTOHERTZ = "fHz"
    ATTOHERTZ = "aHz"
    ZEPTOHERTZ = "zHz"
    YOCTOHERTZ = "yHz"
