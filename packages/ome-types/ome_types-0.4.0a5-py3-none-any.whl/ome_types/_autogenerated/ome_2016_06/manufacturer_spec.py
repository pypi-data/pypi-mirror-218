from typing import Optional

from pydantic import Field

from ome_types._mixins._base_type import OMEType
from ome_types._mixins._kinded import KindMixin

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class ManufacturerSpec(KindMixin, OMEType):
    """This is the base from which many microscope components are extended.

    E.g Objective, Filter etc. Provides attributes for recording common
    properties of these components such as Manufacturer name, Model etc,
    all of which are optional.

    Parameters
    ----------
    manufacturer: The manufacturer of the component. [plain text string]
    model: The Model of the component. [plain text string]
    serial_number: The serial number of the component. [plain text
        string]
    lot_number: The lot number of the component. [plain text string]
    """

    manufacturer: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Manufacturer",
            "type": "Attribute",
        }
    )
    model: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Model",
            "type": "Attribute",
        }
    )
    serial_number: Optional[str] = Field(
        default=None,
        metadata={
            "name": "SerialNumber",
            "type": "Attribute",
        }
    )
    lot_number: Optional[str] = Field(
        default=None,
        metadata={
            "name": "LotNumber",
            "type": "Attribute",
        }
    )
