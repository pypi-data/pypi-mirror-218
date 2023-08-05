from typing import Optional

from pydantic import Field

from ome_types._autogenerated.ome_2016_06.binning import Binning
from ome_types._autogenerated.ome_2016_06.settings import Settings
from ome_types._autogenerated.ome_2016_06.units_electric_potential import (
    UnitsElectricPotential,
)
from ome_types._autogenerated.ome_2016_06.units_frequency import UnitsFrequency

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class DetectorSettings(Settings):
    """This holds the setting applied to a detector as well as a reference to the
    detector.

    The ID is the detector used in this case. The values stored in
    DetectorSettings represent the variable values, fixed values not
    modified during the acquisition go in Detector. Each attribute now
    has an indication of what type of detector it applies to. This is
    preparatory work for cleaning up and possibly splitting this object
    into sub-types.

    Parameters
    ----------
    id:
    offset: The Offset of the detector. [units none] {used:CCD,EMCCD}
    gain: The Gain of the detector. [units:none] {used:CCD,EMCCD,PMT}
    voltage: The Voltage of the detector. {used:PMT} Units are set by
        VoltageUnit.
    voltage_unit: The units of the Voltage of the detector -
        default:volts[V]
    zoom: The Zoom or "Confocal Zoom" or "Scan Zoom" for a detector.
        [units:none] {used:PMT}
    read_out_rate: The speed at which the detector can count pixels.
        {used:CCD,EMCCD} This is the bytes per second that can be read
        from the detector (like a baud rate). Units are set by
        ReadOutRateUnit.
    read_out_rate_unit: The units of the ReadOutRate -
        default:megahertz[Hz].
    binning: Represents the number of pixels that are combined to form
        larger pixels. {used:CCD,EMCCD}
    integration: This is the number of sequential frames that get
        averaged, to improve the signal-to-noise ratio. [units:none]
        {used:CCD,EMCCD}
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    id: str = Field(
        default='__auto_sequence__',
        metadata={
            "name": "ID",
            "type": "Attribute",
            "required": True,
            "pattern": r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Detector:\S+)|(Detector:\S+)",
        },
        regex="(urn:lsid:([\\w\\-\\.]+\\.[\\w\\-\\.]+)+:Detector:\\S+)|(Detector:\\S+)"
    )
    offset: Optional[float] = Field(
        default=None,
        metadata={
            "name": "Offset",
            "type": "Attribute",
        }
    )
    gain: Optional[float] = Field(
        default=None,
        metadata={
            "name": "Gain",
            "type": "Attribute",
        }
    )
    voltage: Optional[float] = Field(
        default=None,
        metadata={
            "name": "Voltage",
            "type": "Attribute",
        }
    )
    voltage_unit: UnitsElectricPotential = Field(
        default=UnitsElectricPotential.VOLT,
        metadata={
            "name": "VoltageUnit",
            "type": "Attribute",
        }
    )
    zoom: Optional[float] = Field(
        default=None,
        metadata={
            "name": "Zoom",
            "type": "Attribute",
        }
    )
    read_out_rate: Optional[float] = Field(
        default=None,
        metadata={
            "name": "ReadOutRate",
            "type": "Attribute",
        }
    )
    read_out_rate_unit: UnitsFrequency = Field(
        default=UnitsFrequency.MEGAHERTZ,
        metadata={
            "name": "ReadOutRateUnit",
            "type": "Attribute",
        }
    )
    binning: Optional[Binning] = Field(
        default=None,
        metadata={
            "name": "Binning",
            "type": "Attribute",
        }
    )
    integration: Optional[int] = Field(
        default=None,
        metadata={
            "name": "Integration",
            "type": "Attribute",
            "min_inclusive": 1,
        },
        ge=1
    )
