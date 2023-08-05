from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class UnitsElectricPotential(Enum):
    """
    The units used to represent an electric potential.

    Properties
    ----------
    YOTTAVOLT: yottavolt unit.
    ZETTAVOLT: zettavolt unit.
    EXAVOLT: exavolt unit.
    PETAVOLT: petavolt unit.
    TERAVOLT: teravolt unit.
    GIGAVOLT: gigavolt unit.
    MEGAVOLT: megavolt unit.
    KILOVOLT: kilovolt unit.
    HECTOVOLT: hectovolt unit.
    DECAVOLT: decavolt unit.
    VOLT: volt unit.
    DECIVOLT: decivolt unit.
    CENTIVOLT: centivolt unit.
    MILLIVOLT: millivolt unit.
    MICROVOLT: microvolt unit.
    NANOVOLT: nanovolt unit.
    PICOVOLT: picovolt unit.
    FEMTOVOLT: femtovolt unit.
    ATTOVOLT: attovolt unit.
    ZEPTOVOLT: zeptovolt unit.
    YOCTOVOLT: yoctovolt unit.
    """

    YOTTAVOLT = "YV"
    ZETTAVOLT = "ZV"
    EXAVOLT = "EV"
    PETAVOLT = "PV"
    TERAVOLT = "TV"
    GIGAVOLT = "GV"
    MEGAVOLT = "MV"
    KILOVOLT = "kV"
    HECTOVOLT = "hV"
    DECAVOLT = "daV"
    VOLT = "V"
    DECIVOLT = "dV"
    CENTIVOLT = "cV"
    MILLIVOLT = "mV"
    MICROVOLT = "µV"
    NANOVOLT = "nV"
    PICOVOLT = "pV"
    FEMTOVOLT = "fV"
    ATTOVOLT = "aV"
    ZEPTOVOLT = "zV"
    YOCTOVOLT = "yV"
