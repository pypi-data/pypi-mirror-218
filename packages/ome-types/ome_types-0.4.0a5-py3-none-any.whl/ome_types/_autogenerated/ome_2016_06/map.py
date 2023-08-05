from typing import List, Optional

from pydantic import Field

from ome_types._mixins._base_type import OMEType

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Map(OMEType):
    """
    This is a Mapping of key/value pairs.

    Parameters
    ----------
    m: This is a key/value pair used to build up a Mapping. The Element
        and Attribute name are kept to single letters to minimize the
        length at the expense of readability as they are likely to occur
        many times.
    """

    ms: List["Map.M"] = Field(
        default_factory=list,
        metadata={
            "name": "M",
            "type": "Element",
            "namespace": "http://www.openmicroscopy.org/Schemas/OME/2016-06",
        }
    )


    class M(OMEType):
        value: str = Field(
            default="",
            metadata={
                "required": True,
            }
        )
        k: Optional[str] = Field(
            default=None,
            metadata={
                "name": "K",
                "type": "Attribute",
            }
        )


M = Map.M
