from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class PixelType(Enum):
    """
    The number size/kind used to represent a pixel.

    Properties
    ----------
    INT8: 8 bit signed integer.
    INT16: 16 bit signed integer.
    INT32: 32 bit signed integer.
    UINT8: 8 bit unsigned integer.
    UINT16: 16 bit unsigned integer.
    UINT32: 32 bit unsigned integer.
    FLOAT: single-precision floating point.
    DOUBLE: double-precision floating point.
    COMPLEXFLOAT: complex single-precision floating point.
    COMPLEXDOUBLE: complex double-precision floating point.
    BIT: bit mask.
    """

    INT8 = "int8"
    INT16 = "int16"
    INT32 = "int32"
    UINT8 = "uint8"
    UINT16 = "uint16"
    UINT32 = "uint32"
    FLOAT = "float"
    DOUBLE = "double"
    COMPLEXFLOAT = "complex"
    COMPLEXDOUBLE = "double-complex"
    BIT = "bit"
