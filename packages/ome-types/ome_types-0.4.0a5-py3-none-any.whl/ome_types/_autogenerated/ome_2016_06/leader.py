from pydantic import Field

from ome_types._autogenerated.ome_2016_06.reference import Reference

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class Leader(Reference):
    """
    Contact information for a ExperimenterGroup leader specified using a reference
    to an Experimenter element defined elsewhere in the document.
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"

    id: str = Field(
        default='__auto_sequence__',
        metadata={
            "name": "ID",
            "type": "Attribute",
            "required": True,
            "pattern": r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Experimenter:\S+)|(Experimenter:\S+)",
        },
        regex="(urn:lsid:([\\w\\-\\.]+\\.[\\w\\-\\.]+)+:Experimenter:\\S+)|(Experimenter:\\S+)"
    )
