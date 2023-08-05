from typing import List, Optional

from pydantic import Field

from ome_types._autogenerated.ome_2016_06.experiment_value import Experiment_value
from ome_types._autogenerated.ome_2016_06.experimenter_ref import ExperimenterRef
from ome_types._autogenerated.ome_2016_06.microbeam_manipulation import (
    MicrobeamManipulation,
)
from ome_types._mixins._base_type import OMEType

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Experiment(OMEType):
    """This element describes the type of experiment.

    The required Type attribute must contain one or more entries from the following list:
    FP FRET Time-lapse 4-D+ Screen Immunocytochemistry FISH Electrophysiology  Ion-Imaging Colocalization PGI/Documentation
    FRAP Photoablation Optical-Trapping Photoactivation Fluorescence-Lifetime Spectral-Imaging Other
    FP refers to fluorescent proteins, PGI/Documentation is not a 'data' image.
    The optional Description element may contain free text to further describe the experiment.

    Parameters
    ----------
    description: A description for the experiment. [plain-text multi-
        line string]
    experimenter_ref: This is a link to the Experimenter who conducted
        the experiment
    microbeam_manipulation:
    type: A term to describe the type of experiment.
    id:
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    description: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "white_space": "preserve",
        }
    )
    experimenter_ref: Optional[ExperimenterRef] = Field(
        default=None,
        metadata={
            "name": "ExperimenterRef",
            "type": "Element",
        }
    )
    microbeam_manipulations: List[MicrobeamManipulation] = Field(
        default_factory=list,
        metadata={
            "name": "MicrobeamManipulation",
            "type": "Element",
        }
    )
    type: List[Experiment_value] = Field(
        default_factory=list,
        metadata={
            "name": "Type",
            "type": "Attribute",
            "tokens": True,
        }
    )
    id: str = Field(
        default='__auto_sequence__',
        metadata={
            "name": "ID",
            "type": "Attribute",
            "required": True,
            "pattern": r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Experiment:\S+)|(Experiment:\S+)",
        },
        regex="(urn:lsid:([\\w\\-\\.]+\\.[\\w\\-\\.]+)+:Experiment:\\S+)|(Experiment:\\S+)"
    )


value = Experiment_value
