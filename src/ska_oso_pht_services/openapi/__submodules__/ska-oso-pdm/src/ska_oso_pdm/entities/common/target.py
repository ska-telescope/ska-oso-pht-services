"""
The entities.common.target module defines a Python representation of the
target of the observation.
"""
import operator
from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable, List, Optional, Union

from astropy.coordinates import Angle, SkyCoord, get_body
from astropy.time import Time

# aliases to str for entity IDs
TargetID = str


class PointingPatternParameters(ABC):
    """
    PointingPatternParameters is an abstract base class extended by classes
    that define receptor pointing patterns.
    """

    @property
    @abstractmethod
    def kind(self):
        raise NotImplementedError


class FivePointParameters(PointingPatternParameters):
    """
    FivePointParameters defines the properties of an observing pattern that
    uses a five-point observing pattern centred on a reference position.
    """

    kind = "FivePointParameters"

    def __init__(self, offset_arcsec: float = 0.0):
        self.offset_arcsec = offset_arcsec

    def __eq__(self, other):
        if not isinstance(other, FivePointParameters):
            return False

        return other.offset_arcsec == self.offset_arcsec

    def __repr__(self):
        return f"<FivePointParameters({self.offset_arcsec})>"


class CrossScanParameters(PointingPatternParameters):
    """
    CrossScanParameters defines the properties of an observing pattern that
    uses a cross scan observing pattern, typically used for pointing
    calibrations.
    """

    kind = "CrossScanParameters"

    def __init__(self, offset_arcsec: float = 0.0):
        self.offset_arcsec = offset_arcsec

    def __eq__(self, other):
        if not isinstance(other, CrossScanParameters):
            return False

        return other.offset_arcsec == self.offset_arcsec

    def __repr__(self):
        return f"<CrossScanParameters({self.offset_arcsec})>"


class SinglePointParameters(PointingPatternParameters):
    """
    SinglePointParameters defines the properties for an observing pattern
    consisting of a single receptor pointing with an optional offset from
    the reference position.
    """

    kind = "SinglePointParameters"

    def __init__(self, offset_x_arcsec: float = 0.0, offset_y_arcsec: float = 0.0):
        self.offset_x_arcsec = offset_x_arcsec
        self.offset_y_arcsec = offset_y_arcsec

    def __eq__(self, other):
        if not isinstance(other, SinglePointParameters):
            return False

        return (
            other.offset_x_arcsec == self.offset_x_arcsec
            and other.offset_y_arcsec == self.offset_y_arcsec
        )

    def __repr__(self):
        return (
            f"<SinglePointParameters({self.offset_x_arcsec}, {self.offset_y_arcsec})>"
        )


class RasterParameters(PointingPatternParameters):
    """
    RasterParameters defines the properties of an observing pattern that
    uses a raster pattern centred on a reference position.
    """

    kind = "RasterParameters"

    def __init__(
        self,
        row_length_arcsec: float = 0.0,
        row_offset_arcsec: float = 0.0,
        n_rows: int = 1,
        pa: float = 0.0,
        unidirectional: bool = False,
    ):
        self.row_length_arcsec = row_length_arcsec
        self.row_offset_arcsec = row_offset_arcsec
        self.n_rows = n_rows
        self.pa = pa
        self.unidirectional = unidirectional

    def __eq__(self, other):
        if not isinstance(other, RasterParameters):
            return False

        return (
            other.row_length_arcsec == self.row_length_arcsec
            and other.row_offset_arcsec == self.row_offset_arcsec
            and other.n_rows == self.n_rows
            and other.pa == self.pa
            and other.unidirectional == self.unidirectional
        )

    def __repr__(self):
        arg_str = f"{self.row_length_arcsec}, {self.row_offset_arcsec}, {self.n_rows}, {self.pa}, {self.unidirectional}"
        return f"<RasterParameters({arg_str})>"


class StarRasterParameters(PointingPatternParameters):
    """
    StarRasterParameters defines the properties of an observing pattern that
    uses a star raster pattern centred on a reference position.
    """

    kind = "StarRasterParameters"

    def __init__(
        self,
        row_length_arcsec: float = 0.0,
        n_rows: int = 1,
        row_offset_angle: float = 0.0,
        unidirectional: bool = False,
    ):
        self.row_length_arcsec = row_length_arcsec
        self.n_rows = n_rows
        self.row_offset_angle = row_offset_angle
        self.unidirectional = unidirectional

    def __eq__(self, other):
        if not isinstance(other, StarRasterParameters):
            return False

        return (
            other.row_length_arcsec == self.row_length_arcsec
            and other.n_rows == self.n_rows
            and other.row_offset_angle == self.row_offset_angle
            and other.unidirectional == self.unidirectional
        )

    def __repr__(self):
        arg_str = f"{self.row_length_arcsec}, {self.n_rows}, {self.row_offset_angle}, {self.unidirectional}"
        return f"<StarRasterParameters({arg_str})>"


class PointingPattern:
    """
    PointingPattern holds the user-configured pointing patterns and current active
    pattern for receptor pointing patterns associated with a target.

    One of each pointing pattern type can be held in the parameters list. Only the
    active pattern will be used for observing; the remainder provide an easy way to
    recover previously edited observing parameters for the target.
    """

    def __init__(
        self,
        active: Optional[str] = None,
        parameters: Optional[List[PointingPatternParameters]] = None,
    ):
        if active is None and parameters is None:
            parameters = [SinglePointParameters()]
            active = SinglePointParameters.kind

        if (active is None) ^ (parameters is None):
            raise ValueError("Must provide active and parameters. Only one specified")

        parameter_kinds = {p.kind for p in parameters}
        # complain if active not in the given parameters or duplicate detected
        if active not in parameter_kinds:
            raise ValueError(
                f"Invalid pointing parameters state: active={active} parameters={parameters}"
            )
        if len(parameter_kinds) != len(parameters):
            raise ValueError(f"Duplicate parameter types in input: {parameters}")

        self.active = active
        self.parameters = parameters

    def __repr__(self):
        return (
            f"<PointingPattern(active={self.active!r}, parameters={self.parameters})>"
        )

    def __eq__(self, other):
        if not isinstance(other, PointingPattern):
            return False

        self_parameters_by_kind = sorted(
            self.parameters, key=operator.attrgetter("kind")
        )
        other_parameters_by_kind = sorted(
            other.parameters, key=operator.attrgetter("kind")
        )

        return (
            other.active == self.active
            and self_parameters_by_kind == other_parameters_by_kind
        )


class Coordinates(ABC):
    """
    Coordinates is an abstract base class for pointing coordinates.
    """

    @property
    @abstractmethod
    def kind(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def coord(self):
        raise NotImplementedError


class Target(ABC):
    """
    Target represents the receptor pointing for an SKA observation, consisting
    of a reference position and a pointing pattern to be used when observing
    the target.

    Default pointing patterns and equatorial coordinates will be set if not
    provided.
    """

    def __init__(
        self,
        target_id: Optional[TargetID] = None,
        pointing_pattern: Optional[PointingPattern] = None,
        reference_coordinate: Optional[Coordinates] = None,
    ):
        if target_id is None:
            target_id = ""
        self.target_id = target_id

        if pointing_pattern is None:
            pointing_pattern = PointingPattern()
        self.pointing_pattern = pointing_pattern

        if reference_coordinate is None:
            reference_coordinate = EquatorialCoordinates()
        self.reference_coordinate = reference_coordinate

    def __eq__(self, other):
        if not isinstance(other, Target):
            return False

        return (
            self.target_id == other.target_id
            and self.pointing_pattern == other.pointing_pattern
            and self.reference_coordinate == other.reference_coordinate
        )

    def __str__(self):
        kind = {
            "SinglePointParameters": "single point",
            "FivePointParameters": "five-point",
            "CrossScanParameters": "cross scan",
        }.get(self.pointing_pattern.active, self.pointing_pattern.active)
        return f"<Target={self.target_id} | {kind} on {self.reference_coordinate.coord.to_string()}>"


class EquatorialCoordinatesReferenceFrame(Enum):
    """
    Enumeration of reference frames supported by an EquatorialCoordinates
    """

    ICRS = "icrs"
    FK5 = "fk5"


class EquatorialCoordinates(Coordinates):
    """
    SiderealTarget represents the argument for SKA scheduling block.
    """

    kind = "equatorial"

    EQUALITY_TOLERANCE = Angle(6e-17, unit="rad")  # Arbitrary small angle

    #  pylint: disable=too-many-arguments
    def __init__(
        self,
        ra: Optional[Union[float, str]] = 0.0,
        dec: Optional[Union[float, str]] = 0.0,
        reference_frame: Optional[
            EquatorialCoordinatesReferenceFrame
        ] = EquatorialCoordinatesReferenceFrame.ICRS,
        unit: Union[str, Iterable[str]] = ("hourangle", "deg"),
    ):
        super().__init__()
        self.ra = ra
        self.dec = dec
        self.reference_frame = reference_frame
        self.unit = _reformat_unit(unit)

        # astropy demands a string for single unit coords
        str_unit = ",".join(self.unit)
        self._coord = SkyCoord(
            self.ra, self.dec, unit=str_unit, frame=self.reference_frame.value
        )

    @property
    def coord(self):
        return self._coord

    def __eq__(self, other):
        if not isinstance(other, EquatorialCoordinates):
            return False

        # Please replace this with a more elegant way of dealing with differences
        # due to floating point arithmetic when comparing targets
        # defined in different ways.
        return (
            self.coord.frame.name == other.coord.frame.name
            and self.coord.separation(other.coord) < self.EQUALITY_TOLERANCE
        )

    def __repr__(self):
        raw_ra = self.coord.ra.value
        raw_dec = self.coord.dec.value
        units = (self.coord.ra.unit.name, self.coord.dec.unit.name)
        reference_frame = self.reference_frame
        return f"<EquatorialCoordinates(ra={raw_ra}, dec={raw_dec}, frame={reference_frame.name}, unit={units})>"

    def __str__(self):
        return (
            f"<EquatorialCoordinates: "
            f'({self.coord.to_string(style="hmsdms")} {self.reference_frame.name})>'
        )


class HorizontalCoordinatesReferenceFrame(Enum):
    """
    Enumeration of reference frames supported by a HorizontalCoordinates.
    """

    ALTAZ = "altaz"


class HorizontalCoordinates(Coordinates):
    """
    DriftScanTarget defines AltAz target for SKA scheduling block.
    """

    kind = "horizontal"

    EQUALITY_TOLERANCE = Angle(6e-17, unit="rad")  # Arbitrary small angle

    #  pylint: disable=too-many-arguments
    def __init__(
        self,
        az: float,
        el: float,
        unit: Optional[Union[str, Iterable[str]]] = "deg",
        reference_frame: Optional[
            HorizontalCoordinatesReferenceFrame
        ] = HorizontalCoordinatesReferenceFrame.ALTAZ,
    ):
        super().__init__()
        self.az = az
        self.el = el
        self.reference_frame = reference_frame
        self.unit = _reformat_unit(unit)

        # astropy demands a string for single unit coords
        str_unit = ",".join(self.unit)
        self._coord = SkyCoord(
            az=az, alt=el, unit=str_unit, frame=reference_frame.value
        )

    @property
    def coord(self):
        return self._coord

    def __eq__(self, other):
        if not isinstance(other, HorizontalCoordinates):
            return False

        return (
            self.coord.frame.name == other.coord.frame.name
            and self.coord.separation(other.coord) < self.EQUALITY_TOLERANCE
        )

    def __repr__(self):
        raw_az = self.coord.az.value
        raw_alt = self.coord.alt.value
        units = (self.coord.az.unit.name, self.coord.alt.unit.name)
        reference_frame = self.reference_frame.name
        return f"<HorizontalCoordinates(az={raw_az}, el={raw_alt}, unit={units}, reference_frame={reference_frame})>"

    def __str__(self):
        return f"<HorizontalCoordinates: ({self.coord.to_string()} {self.reference_frame.name})>"


class SolarSystemObjectName(Enum):
    """
    SolarSystemObjectName represents name of the solar system object.
    """

    MERCURY = "mercury"
    VENUS = "venus"
    MARS = "mars"


class SolarSystemObject(Coordinates):
    """
    Planet represents the argument for SKA scheduling block.
    """

    kind = "sso"

    def __init__(self, name: SolarSystemObjectName):
        self.name = name

    @property
    def coord(self):  # pylint: disable=invalid-overridden-method
        return get_body(self.name.value, Time.now())

    def __eq__(self, other):
        if not isinstance(other, SolarSystemObject):
            return False

        return self.name == other.name

    def __repr__(self):
        return f"<SolarSystemObject({self.name})>"

    def __str__(self):
        return f"<SolarSystemObject: {self.name.value}>"


def _reformat_unit(unit: Union[str, Iterable[str]]) -> List[str]:
    """
    Reformats a string or tuple of strings to a standard unit format
    acceptable to astropy.
    """
    if isinstance(unit, str):
        unit = list(unit.split(","))
    return unit
