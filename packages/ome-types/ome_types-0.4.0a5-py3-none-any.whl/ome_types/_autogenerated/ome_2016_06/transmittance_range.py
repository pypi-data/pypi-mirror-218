from typing import Optional

from pydantic import Field

from ome_types._autogenerated.ome_2016_06.units_length import UnitsLength
from ome_types._mixins._base_type import OMEType

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class TransmittanceRange(OMEType):
    """This records the range of wavelengths that are transmitted by the filter.

    It also records the maximum amount of light transmitted.

    Parameters
    ----------
    cut_in: CutIn is the wavelength below which there is less than 50%
        transmittance for a filter. Units are set by CutInUnit.
    cut_in_unit: The units of the CutIn - default:nanometres[nm].
    cut_out: CutOut is the wavelength above which there is less than 50%
        transmittance for a filter. Units are set by CutOutUnit.
    cut_out_unit: The units of the CutOut - default:nanometres[nm].
    cut_in_tolerance: CutInTolerance. Units are set by
        CutInToleranceUnit.
    cut_in_tolerance_unit: The units of the CutInTolerance -
        default:nanometres[nm].
    cut_out_tolerance: CutOutTolerance. Units are set by
        CutOutToleranceUnit.
    cut_out_tolerance_unit: The units of the CutOutTolerance -
        default:nanometres[nm].
    transmittance: The amount of light the filter transmits at a maximum
        [units:none] A fraction, as a value from 0.0 to 1.0.
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    cut_in: Optional[float] = Field(
        default=None,
        metadata={
            "name": "CutIn",
            "type": "Attribute",
            "min_exclusive": 0.0,
        },
        gt=0.0
    )
    cut_in_unit: UnitsLength = Field(
        default=UnitsLength.NANOMETER,
        metadata={
            "name": "CutInUnit",
            "type": "Attribute",
        }
    )
    cut_out: Optional[float] = Field(
        default=None,
        metadata={
            "name": "CutOut",
            "type": "Attribute",
            "min_exclusive": 0.0,
        },
        gt=0.0
    )
    cut_out_unit: UnitsLength = Field(
        default=UnitsLength.NANOMETER,
        metadata={
            "name": "CutOutUnit",
            "type": "Attribute",
        }
    )
    cut_in_tolerance: Optional[float] = Field(
        default=None,
        metadata={
            "name": "CutInTolerance",
            "type": "Attribute",
            "min_inclusive": 0.0,
        },
        ge=0.0
    )
    cut_in_tolerance_unit: UnitsLength = Field(
        default=UnitsLength.NANOMETER,
        metadata={
            "name": "CutInToleranceUnit",
            "type": "Attribute",
        }
    )
    cut_out_tolerance: Optional[float] = Field(
        default=None,
        metadata={
            "name": "CutOutTolerance",
            "type": "Attribute",
            "min_inclusive": 0.0,
        },
        ge=0.0
    )
    cut_out_tolerance_unit: UnitsLength = Field(
        default=UnitsLength.NANOMETER,
        metadata={
            "name": "CutOutToleranceUnit",
            "type": "Attribute",
        }
    )
    transmittance: Optional[float] = Field(
        default=None,
        metadata={
            "name": "Transmittance",
            "type": "Attribute",
            "min_inclusive": 0.0,
            "max_inclusive": 1.0,
        },
        ge=0.0,
        le=1.0
    )
