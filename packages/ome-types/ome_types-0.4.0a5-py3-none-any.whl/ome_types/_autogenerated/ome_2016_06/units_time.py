from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class UnitsTime(Enum):
    """
    The units used to represent a time interval.

    Properties
    ----------
    YOTTASECOND: yottasecond SI unit.
    ZETTASECOND: zettasecond SI unit.
    EXASECOND: exasecond SI unit.
    PETASECOND: petasecond SI unit.
    TERASECOND: terasecond SI unit.
    GIGASECOND: gigasecond SI unit.
    MEGASECOND: megasecond SI unit.
    KILOSECOND: kilosecond SI unit.
    HECTOSECOND: hectosecond SI unit.
    DECASECOND: decasecond SI unit.
    SECOND: second SI unit.
    DECISECOND: decisecond SI unit.
    CENTISECOND: centisecond SI unit.
    MILLISECOND: millisecond SI unit.
    MICROSECOND: microsecond SI unit.
    NANOSECOND: nanosecond SI unit.
    PICOSECOND: picosecond SI unit.
    FEMTOSECOND: femtosecond SI unit.
    ATTOSECOND: attosecond SI unit.
    ZEPTOSECOND: zeptosecond SI unit.
    YOCTOSECOND: yoctosecond SI unit.
    MINUTE: minute SI-derived unit.
    HOUR: hour SI-derived unit.
    DAY: day SI-derived unit.
    """

    YOTTASECOND = "Ys"
    ZETTASECOND = "Zs"
    EXASECOND = "Es"
    PETASECOND = "Ps"
    TERASECOND = "Ts"
    GIGASECOND = "Gs"
    MEGASECOND = "Ms"
    KILOSECOND = "ks"
    HECTOSECOND = "hs"
    DECASECOND = "das"
    SECOND = "s"
    DECISECOND = "ds"
    CENTISECOND = "cs"
    MILLISECOND = "ms"
    MICROSECOND = "µs"
    NANOSECOND = "ns"
    PICOSECOND = "ps"
    FEMTOSECOND = "fs"
    ATTOSECOND = "as"
    ZEPTOSECOND = "zs"
    YOCTOSECOND = "ys"
    MINUTE = "min"
    HOUR = "h"
    DAY = "d"
