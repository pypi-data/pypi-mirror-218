
from ome_types._autogenerated.ome_2016_06.light_source import LightSource

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class LightEmittingDiode(LightSource):
    """The LightEmittingDiode element is used to describe various kinds of LED
    lamps. As the LightEmittingDiode is inside a LightSource it already has
    available the values from ManufacturerSpec (Manufacturer, Model, SerialNumber,
    LotNumber) And the values from LightSource which includes Power in milliwatts
    We have looked at extending this element but have had a problem producing a
    generic solution.

    Possible attributes talked about adding include:
    Power in lumens - but this is complicated by multi-channel
    devices like CoolLED where each channel's power is different
    Wavelength Range - not a simple value so would require
    multiple attributes or a child element
    Angle of Projection - this would be further affected by the
    optics used for filtering the naked LED or that combine
    power from multiple devices
    These values are further affected if you over-drive the LED
    resulting in a more complex system
    Another issue is that LED's may not be used directly for
    illumination but as drivers for secondary emissions from doped
    fiber optics. This would require the fiber optics to be modeled.
    Thanks to Paul Goodwin of Applied Precision of information about
    this topic.
    """

    class Meta:
        namespace = "http://www.openmicroscopy.org/Schemas/OME/2016-06"
