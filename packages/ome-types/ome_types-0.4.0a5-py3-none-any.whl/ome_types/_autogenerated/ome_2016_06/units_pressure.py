from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class UnitsPressure(Enum):
    """
    The units used to represent a pressure.

    Properties
    ----------
    YOTTAPASCAL: yottapascal SI unit.
    ZETTAPASCAL: zettapascal SI unit.
    EXAPASCAL: exapascal SI unit.
    PETAPASCAL: petapascal SI unit.
    TERAPASCAL: terapascal SI unit.
    GIGAPASCAL: gigapascal SI unit.
    MEGAPASCAL: megapascal SI unit.
    KILOPASCAL: kilopascal SI unit.
    HECTOPASCAL: hectopascal SI unit.
    DECAPASCAL: decapascal SI unit.
    PASCAL: pascal SI unit.  Note the C++ enum is mixed case due to
        PASCAL being a macro used by the Microsoft C and C++ compiler.
    DECIPASCAL: decipascal SI unit.
    CENTIPASCAL: centipascal SI unit.
    MILLIPASCAL: millipascal SI unit.
    MICROPASCAL: micropascal SI unit.
    NANOPASCAL: nanopascal SI unit.
    PICOPASCAL: picopascal SI unit.
    FEMTOPASCAL: femtopascal SI unit.
    ATTOPASCAL: attopascal SI unit.
    ZEPTOPASCAL: zeptopascal SI unit.
    YOCTOPASCAL: yoctopascal SI unit.
    BAR: bar SI-derived unit.
    MEGABAR: megabar SI-derived unit.
    KILOBAR: kilobar SI-derived unit.
    DECIBAR: decibar SI-derived unit.
    CENTIBAR: centibar SI-derived unit.
    MILLIBAR: millibar SI-derived unit.
    ATMOSPHERE: standard atmosphere SI-derived unit.
    PSI: pound-force per square inch Imperial unit.
    TORR: torr SI-derived unit.
    MILLITORR: millitorr SI-derived unit.
    MMHG: millimetre of mercury SI-derived unit
    """

    YOTTAPASCAL = "YPa"
    ZETTAPASCAL = "ZPa"
    EXAPASCAL = "EPa"
    PETAPASCAL = "PPa"
    TERAPASCAL = "TPa"
    GIGAPASCAL = "GPa"
    MEGAPASCAL = "MPa"
    KILOPASCAL = "kPa"
    HECTOPASCAL = "hPa"
    DECAPASCAL = "daPa"
    PASCAL = "Pa"
    DECIPASCAL = "dPa"
    CENTIPASCAL = "cPa"
    MILLIPASCAL = "mPa"
    MICROPASCAL = "µPa"
    NANOPASCAL = "nPa"
    PICOPASCAL = "pPa"
    FEMTOPASCAL = "fPa"
    ATTOPASCAL = "aPa"
    ZEPTOPASCAL = "zPa"
    YOCTOPASCAL = "yPa"
    BAR = "bar"
    MEGABAR = "Mbar"
    KILOBAR = "kbar"
    DECIBAR = "dbar"
    CENTIBAR = "cbar"
    MILLIBAR = "mbar"
    ATMOSPHERE = "atm"
    PSI = "psi"
    TORR = "Torr"
    MILLITORR = "mTorr"
    MMHG = "mm Hg"
