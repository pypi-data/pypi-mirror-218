from typing import Optional

from pydantic import Field

from ome_types._autogenerated.ome_2016_06.filament_type import Filament_Type
from ome_types._autogenerated.ome_2016_06.light_source import LightSource

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Filament(LightSource):
    """The Filament element is used to describe various kinds of filament bulbs
    such as Incadescent or Halogen.

    The Power of the Filament is now stored in the LightSource.

    Parameters
    ----------
    type: The type of filament.
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    type: Optional[Filament_Type] = Field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Attribute",
        }
    )


Type = Filament_Type
