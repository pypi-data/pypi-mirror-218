from enum import Enum

__NAMESPACE__ = "http://www.openmicroscopy.org/Schemas/OME/2016-06"


class UnitsLength(Enum):
    """
    The units used to represent a length.

    Properties
    ----------
    YOTTAMETER: yottameter SI unit.
    ZETTAMETER: zettameter SI unit.
    EXAMETER: exameter SI unit.
    PETAMETER: petameter SI unit.
    TERAMETER: terameter SI unit.
    GIGAMETER: gigameter SI unit.
    MEGAMETER: megameter SI unit.
    KILOMETER: kilometer SI unit.
    HECTOMETER: hectometer SI unit.
    DECAMETER: decameter SI unit.
    METER: meter SI unit.
    DECIMETER: decimeter SI unit.
    CENTIMETER: centimeter SI unit.
    MILLIMETER: millimeter SI unit.
    MICROMETER: micrometer SI unit.
    NANOMETER: nanometer SI unit.
    PICOMETER: picometer SI unit.
    FEMTOMETER: femtometer SI unit.
    ATTOMETER: attometer SI unit.
    ZEPTOMETER: zeptometer SI unit.
    YOCTOMETER: yoctometer SI unit.
    ANGSTROM: ångström SI-derived unit.
    THOU: thou Imperial unit (or mil, 1/1000 inch).
    LINE: line Imperial unit (1/12 inch).
    INCH: inch Imperial unit.
    FOOT: foot Imperial unit.
    YARD: yard Imperial unit.
    MILE: terrestrial mile Imperial unit.
    ASTRONOMICALUNIT: astronomical unit SI-derived unit. The official
        term is ua as the SI standard assigned AU to absorbance unit.
    LIGHTYEAR: light year.
    PARSEC: parsec.
    POINT: typography point Imperial-derived unit (1/72 inch). Use of
        this unit should be limited to font sizes.
    PIXEL: pixel abstract unit.  This is not convertible to any other
        length unit without a calibrated scaling factor. Its use should
        should be limited to ROI objects, and converted to an
        appropriate length units using the PhysicalSize units of the
        Image the ROI is attached to.
    REFERENCEFRAME: reference frame abstract unit.  This is not
        convertible to any other length unit without a scaling factor.
        Its use should be limited to uncalibrated stage positions, and
        converted to an appropriate length unit using a calibrated
        scaling factor.
    """

    YOTTAMETER = "Ym"
    ZETTAMETER = "Zm"
    EXAMETER = "Em"
    PETAMETER = "Pm"
    TERAMETER = "Tm"
    GIGAMETER = "Gm"
    MEGAMETER = "Mm"
    KILOMETER = "km"
    HECTOMETER = "hm"
    DECAMETER = "dam"
    METER = "m"
    DECIMETER = "dm"
    CENTIMETER = "cm"
    MILLIMETER = "mm"
    MICROMETER = "µm"
    NANOMETER = "nm"
    PICOMETER = "pm"
    FEMTOMETER = "fm"
    ATTOMETER = "am"
    ZEPTOMETER = "zm"
    YOCTOMETER = "ym"
    ANGSTROM = "Å"
    THOU = "thou"
    LINE = "li"
    INCH = "in"
    FOOT = "ft"
    YARD = "yd"
    MILE = "mi"
    ASTRONOMICALUNIT = "ua"
    LIGHTYEAR = "ly"
    PARSEC = "pc"
    POINT = "pt"
    PIXEL = "pixel"
    REFERENCEFRAME = "reference frame"
