from typing import Optional

from pydantic import Field

from ome_types._autogenerated.ome_2016_06.bin_data import BinData
from ome_types._autogenerated.ome_2016_06.external import External
from ome_types._mixins._base_type import OMEType

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class BinaryFile(OMEType):
    """
    Describes a binary file.

    Parameters
    ----------
    external:
    bin_data:
    file_name:
    size: Size of the uncompressed file. [unit:bytes]
    mime_type:
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    external: Optional[External] = Field(
        default=None,
        metadata={
            "name": "External",
            "type": "Element",
        }
    )
    bin_data: Optional[BinData] = Field(
        default=None,
        metadata={
            "name": "BinData",
            "type": "Element",
        }
    )
    file_name: str = Field(
        metadata={
            "name": "FileName",
            "type": "Attribute",
            "required": True,
        }
    )
    size: int = Field(
        metadata={
            "name": "Size",
            "type": "Attribute",
            "required": True,
            "min_inclusive": 0,
        },
        ge=0
    )
    mime_type: Optional[str] = Field(
        default=None,
        metadata={
            "name": "MIMEType",
            "type": "Attribute",
        }
    )
