from typing import List, Optional

from pydantic import Field

from ome_types._autogenerated.ome_2016_06.annotation_ref import AnnotationRef
from ome_types._autogenerated.ome_2016_06.arc import Arc
from ome_types._autogenerated.ome_2016_06.detector import Detector
from ome_types._autogenerated.ome_2016_06.dichroic import Dichroic
from ome_types._autogenerated.ome_2016_06.filament import Filament
from ome_types._autogenerated.ome_2016_06.filter import Filter
from ome_types._autogenerated.ome_2016_06.filter_set import FilterSet
from ome_types._autogenerated.ome_2016_06.generic_excitation_source import (
    GenericExcitationSource,
)
from ome_types._autogenerated.ome_2016_06.laser import Laser
from ome_types._autogenerated.ome_2016_06.light_emitting_diode import LightEmittingDiode
from ome_types._autogenerated.ome_2016_06.microscope import Microscope
from ome_types._autogenerated.ome_2016_06.objective import Objective
from ome_types._mixins._base_type import OMEType
from ome_types._mixins._instrument import InstrumentMixin

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Instrument(OMEType, InstrumentMixin):
    """This element describes the instrument used to capture the Image.

    It is primarily a container for manufacturer's model and catalog
    numbers for the Microscope, LightSource, Detector, Objective and
    Filters components. The Objective element contains the additional
    elements LensNA and Magnification. The Filters element can be
    composed either of separate excitation, emission filters and a
    dichroic mirror or a single filter set. Within the Image itself, a
    reference is made to this one Filter element. There may be multiple
    light sources, detectors, objectives and filters on a microscope.
    Each of these has their own ID attribute, which can be referred to
    from Channel. It is understood that the light path configuration can
    be different for each channel, but cannot be different for each
    timepoint or each plane of an XYZ stack.
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    microscope: Optional[Microscope] = Field(
        default=None,
        metadata={
            "name": "Microscope",
            "type": "Element",
        }
    )
    generic_excitation_sources: List[GenericExcitationSource] = Field(
        default_factory=list,
        metadata={
            "name": "GenericExcitationSource",
            "type": "Element",
        }
    )
    light_emitting_diodes: List[LightEmittingDiode] = Field(
        default_factory=list,
        metadata={
            "name": "LightEmittingDiode",
            "type": "Element",
        }
    )
    filaments: List[Filament] = Field(
        default_factory=list,
        metadata={
            "name": "Filament",
            "type": "Element",
        }
    )
    arcs: List[Arc] = Field(
        default_factory=list,
        metadata={
            "name": "Arc",
            "type": "Element",
        }
    )
    lasers: List[Laser] = Field(
        default_factory=list,
        metadata={
            "name": "Laser",
            "type": "Element",
        }
    )
    detectors: List[Detector] = Field(
        default_factory=list,
        metadata={
            "name": "Detector",
            "type": "Element",
        }
    )
    objectives: List[Objective] = Field(
        default_factory=list,
        metadata={
            "name": "Objective",
            "type": "Element",
        }
    )
    filter_sets: List[FilterSet] = Field(
        default_factory=list,
        metadata={
            "name": "FilterSet",
            "type": "Element",
        }
    )
    filters: List[Filter] = Field(
        default_factory=list,
        metadata={
            "name": "Filter",
            "type": "Element",
        }
    )
    dichroics: List[Dichroic] = Field(
        default_factory=list,
        metadata={
            "name": "Dichroic",
            "type": "Element",
        }
    )
    annotation_refs: List[AnnotationRef] = Field(
        default_factory=list,
        metadata={
            "name": "AnnotationRef",
            "type": "Element",
        }
    )
    id: str = Field(
        default='__auto_sequence__',
        metadata={
            "name": "ID",
            "type": "Attribute",
            "required": True,
            "pattern": r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Instrument:\S+)|(Instrument:\S+)",
        },
        regex="(urn:lsid:([\\w\\-\\.]+\\.[\\w\\-\\.]+)+:Instrument:\\S+)|(Instrument:\\S+)"
    )
