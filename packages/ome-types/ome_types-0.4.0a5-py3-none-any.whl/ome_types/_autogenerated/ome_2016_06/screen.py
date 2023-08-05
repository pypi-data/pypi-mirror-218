from typing import List, Optional

from pydantic import Field

from ome_types._autogenerated.ome_2016_06.annotation_ref import AnnotationRef
from ome_types._autogenerated.ome_2016_06.reagent import Reagent
from ome_types._autogenerated.ome_2016_06.reference import Reference
from ome_types._mixins._base_type import OMEType

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Screen(OMEType):
    """The Screen element is a grouping for Plates.

    The required attribute is the Screen's Name and ID - both must be unique within the document.
    The Screen element may contain an ExternalRef attribute that refers to an external database.
    A description of the screen may be specified in the Description element.
    Screens may contain overlapping sets of Plates i.e.      Screens and Plates have a many-to-many relationship.
    Plates contain one or more ScreenRef elements to specify what screens they belong to.

    Parameters
    ----------
    description: A description for the screen.
    reagent:
    plate_ref: The PlateRef element is a reference to a Plate element.
        Screen elements may have one or more PlateRef elements to define
        the plates that are part of the screen. Plates may belong to
        more than one screen.
    annotation_ref:
    id:
    name:
    protocol_identifier: A pointer to an externally defined protocol,
        usually in a screening database.
    protocol_description: A description of the screen protocol; may
        contain very detailed information to reproduce some of that
        found in a screening database.
    reagent_set_description: A description of the set of reagents; may
        contain very detailed information to reproduce some of that
        information found in a screening database.
    reagent_set_identifier: A pointer to an externally defined set of
        reagents, usually in a screening database/automation database.
    type: A human readable identifier for the screen type; e.g. RNAi,
        cDNA, SiRNA, etc. This string is likely to become an enumeration
        in future releases.
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
    reagents: List[Reagent] = Field(
        default_factory=list,
        metadata={
            "name": "Reagent",
            "type": "Element",
        }
    )
    plate_refs: List["Screen.PlateRef"] = Field(
        default_factory=list,
        metadata={
            "name": "PlateRef",
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
            "pattern": r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Screen:\S+)|(Screen:\S+)",
        },
        regex="(urn:lsid:([\\w\\-\\.]+\\.[\\w\\-\\.]+)+:Screen:\\S+)|(Screen:\\S+)"
    )
    name: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
        }
    )
    protocol_identifier: Optional[str] = Field(
        default=None,
        metadata={
            "name": "ProtocolIdentifier",
            "type": "Attribute",
        }
    )
    protocol_description: Optional[str] = Field(
        default=None,
        metadata={
            "name": "ProtocolDescription",
            "type": "Attribute",
        }
    )
    reagent_set_description: Optional[str] = Field(
        default=None,
        metadata={
            "name": "ReagentSetDescription",
            "type": "Attribute",
        }
    )
    reagent_set_identifier: Optional[str] = Field(
        default=None,
        metadata={
            "name": "ReagentSetIdentifier",
            "type": "Attribute",
        }
    )
    type: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Attribute",
        }
    )


    class PlateRef(Reference):
        id: str = Field(
            default='__auto_sequence__',
            metadata={
                "name": "ID",
                "type": "Attribute",
                "required": True,
                "pattern": r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Plate:\S+)|(Plate:\S+)",
            },
            regex="(urn:lsid:([\\w\\-\\.]+\\.[\\w\\-\\.]+)+:Plate:\\S+)|(Plate:\\S+)"
        )


PlateRef = Screen.PlateRef
