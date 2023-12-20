"""
Unit tests for the ska_oso_pdm.entities.common.target module.
"""
import copy

import pytest
from astropy.coordinates import SkyCoord

from ska_oso_pdm.entities.common.target import (
    Coordinates,
    CrossScanParameters,
    EquatorialCoordinates,
    EquatorialCoordinatesReferenceFrame,
    FivePointParameters,
    HorizontalCoordinates,
    PointingPattern,
    PointingPatternParameters,
    RasterParameters,
    SinglePointParameters,
    SolarSystemObject,
    SolarSystemObjectName,
    StarRasterParameters,
    Target,
)

COORD = SkyCoord(ra=1, dec=0.5, frame="icrs", unit=("hourangle", "deg"))


def test_cannot_instantiate_coordinates():
    """
    Should not be able to create an instance of an abstract Coordinate
    """
    with pytest.raises(TypeError):
        Coordinates()  # pylint: disable=abstract-class-instantiated


def test_cannot_instantiate_pointingpatternparameters():
    """
    Should not be able to create an instance of an abstract PointingPatternParameters
    """
    with pytest.raises(TypeError):
        PointingPatternParameters()  # pylint: disable=abstract-class-instantiated


class TestEquatorialCoordinates:
    def test_defaults(self):
        """
        Verify EquatorialCoordinates default arguments.
        """
        target_1 = EquatorialCoordinates(ra=1, dec=0.5)
        target_2 = EquatorialCoordinates(
            ra=1,
            dec=0.5,
            reference_frame=EquatorialCoordinatesReferenceFrame.ICRS,
            unit=("hourangle", "deg"),
        )
        assert target_1 == target_2

    def test_eq(self):
        """
        Verify that EquatorialCoordinates objects are considered equal when:

          - they point to the same place on the sky
          - they use the same co-ordinate frame
          - they use the same co-ordinate units
        """
        target_1 = EquatorialCoordinates(
            ra=1,
            dec=2,
            reference_frame=EquatorialCoordinatesReferenceFrame.FK5,
            unit="deg",
        )
        target_2 = EquatorialCoordinates(
            ra=1,
            dec=2,
            reference_frame=EquatorialCoordinatesReferenceFrame.FK5,
            unit="deg",
        )
        target_3 = EquatorialCoordinates(ra=1, dec=1)
        assert target_1 == target_2
        assert target_1 != target_3

    def test_not_equal_to_other_objects(self):
        """
        Verify that EquatorialCoordinates objects are considered unequal to other objects.
        """
        target = EquatorialCoordinates(
            ra=1,
            dec=2,
            reference_frame=EquatorialCoordinatesReferenceFrame.FK5,
            unit="deg",
        )
        assert target != object

    def test_repr(self):
        """
        Verify the repr representation of a Target.
        """
        target = EquatorialCoordinates(
            ra=30,
            dec=-3600,
            reference_frame=EquatorialCoordinatesReferenceFrame.ICRS,
            unit=("deg", "arcsec"),
        )
        expected = "<EquatorialCoordinates(ra=30.0, dec=-1.0, frame=ICRS, unit=('deg', 'deg'))>"
        assert expected == repr(target)

    def test_str(self):
        """
        Verify the string representation of a EquatorialCoordinates.
        """
        target = EquatorialCoordinates(
            ra=30,
            dec="0",
            reference_frame=EquatorialCoordinatesReferenceFrame.ICRS,
            unit=("deg", "rad"),
        )
        expected = "<EquatorialCoordinates: (02h00m00s +00d00m00s ICRS)>"
        assert expected == str(target)


class TestHorizontalCoordinates:
    def test_defaults(self):
        """
        Verify HorizontalCoordinates default arguments.
        """
        target_1 = HorizontalCoordinates(az=1, el=0.5)
        target_2 = HorizontalCoordinates(az=1, el=0.5, unit=("deg", "deg"))
        assert target_1 == target_2

    def test_eq(self):
        """
        Verify that HorizontalCoordinates objects are considered equal when:

          - they point to the same place on the sky
        """
        target_1 = HorizontalCoordinates(az=1, el=2)
        target_2 = HorizontalCoordinates(az=1, el=2)
        target_3 = HorizontalCoordinates(az=1, el=1)
        assert target_1 == target_2
        assert target_1 != target_3

    def test_not_equal_to_other_objects(self):
        """
        Verify that HorizontalCoordinates objects are considered unequal to other objects.
        """
        target = HorizontalCoordinates(az=1, el=2)
        assert target != object

    def test_repr(self):
        """
        Verify the repr representation of a HorizontalCoordinates.
        """
        target = HorizontalCoordinates(az=180.0, el=45.0, unit="deg")
        expected = (
            "<HorizontalCoordinates(az=180.0, el=45.0, unit=('deg', 'deg'), "
            "reference_frame=ALTAZ)>"
        )
        assert expected == repr(target)

    def test_str(self):
        """
        Verify the string representation of a HorizontalCoordinates.
        """
        target = HorizontalCoordinates(az=180.0, el=45.0, unit="deg")
        expected = "<HorizontalCoordinates: (180 45 ALTAZ)>"
        assert expected == str(target)


class TestSolarSystemObject:
    def test_eq(self):
        """
        Verify that SolarSystemObject instances are considered equal when:

          - they point to the same planet
        """
        target_1 = SolarSystemObject(SolarSystemObjectName.MARS)
        target_2 = SolarSystemObject(SolarSystemObjectName.MARS)
        target_3 = SolarSystemObject(SolarSystemObjectName.VENUS)
        assert target_1 == target_2
        assert target_1 != target_3

    def test_is_not_equal_to_other_objects(self):
        """
        Verify that EquatorialCoordinates objects are considered unequal to other objects.
        """
        planet = SolarSystemObject(SolarSystemObjectName.MARS)
        assert planet != EquatorialCoordinates(ra=0, dec=0)
        assert planet != object

    def test_repr(self):
        """
        Verify the repr representation of a SolarSystemObject.
        """
        mars = SolarSystemObject(SolarSystemObjectName.MARS)
        expected = "<SolarSystemObject(SolarSystemObjectName.MARS)>"
        assert repr(mars) == expected

    def test_str(self):
        """
        Verify the string representation of a SolarSystemObject.
        """
        mars = SolarSystemObject(SolarSystemObjectName.MARS)
        expected = "<SolarSystemObject: mars>"
        assert str(mars) == expected


class TestCrossScanParameters:
    def test_defaults(self):
        x = CrossScanParameters()
        y = CrossScanParameters(0.0)
        assert x == y

    def test_eq(self):
        x = CrossScanParameters(1.0)
        y = CrossScanParameters(1.0)
        z = CrossScanParameters(0.0)
        assert x == y
        assert y == x
        assert z != x

    def test_not_eq_to_other_objects(self):
        x = CrossScanParameters(1.0)
        y = FivePointParameters(1.0)
        assert x != y

    def test_repr(self):
        x = CrossScanParameters(1.0)
        assert repr(x) == "<CrossScanParameters(1.0)>"


class TestFivePointParameters:
    def test_defaults(self):
        x = FivePointParameters()
        y = FivePointParameters(0.0)
        assert x == y

    def test_eq(self):
        x = FivePointParameters(1.0)
        y = FivePointParameters(1.0)
        z = FivePointParameters(0.0)
        assert x == y
        assert y == x
        assert z != x

    def test_not_eq_to_other_objects(self):
        x = FivePointParameters(1.0)
        y = CrossScanParameters(1.0)
        assert x != y

    def test_repr(self):
        x = FivePointParameters(1.0)
        assert repr(x) == "<FivePointParameters(1.0)>"


class TestSinglePointParameters:
    def test_defaults(self):
        x = SinglePointParameters()
        y = SinglePointParameters(0.0, 0.0)
        assert x == y

    def test_eq(self):
        x = SinglePointParameters(1.0, 1.0)
        assert x == SinglePointParameters(1.0, 1.0)
        assert x != SinglePointParameters(1.0, 0.0)
        assert x != SinglePointParameters(0.0, 1.0)

    def test_not_eq_to_other_objects(self):
        x = SinglePointParameters()
        assert x != CrossScanParameters()
        assert x != object

    def test_repr(self):
        x = SinglePointParameters()
        assert repr(x) == "<SinglePointParameters(0.0, 0.0)>"


class TestRasterParameters:
    def test_defaults(self):
        x = RasterParameters()
        y = RasterParameters(
            row_length_arcsec=0.0,
            row_offset_arcsec=0.0,
            n_rows=1,
            pa=0.0,
            unidirectional=False,
        )
        assert x == y

    def test_eq(self):
        x = RasterParameters()
        y = RasterParameters()
        assert x == y

        non_defaults = dict(
            row_length_arcsec=1.0,
            row_offset_arcsec=1.0,
            n_rows=2,
            pa=1.0,
            unidirectional=True,
        )
        for k, v in non_defaults.items():
            y = RasterParameters()
            setattr(y, k, v)
            assert y != x

    def test_not_eq_to_other_objects(self):
        x = RasterParameters()
        y = CrossScanParameters()
        assert x != y

    def test_repr(self):
        x = RasterParameters()
        assert repr(x) == "<RasterParameters(0.0, 0.0, 1, 0.0, False)>"


class TestStarRasterParameters:
    def test_defaults(self):
        x = StarRasterParameters()
        y = StarRasterParameters(
            row_length_arcsec=0.0, n_rows=1, row_offset_angle=0.0, unidirectional=False
        )
        assert x == y

    def test_eq(self):
        x = StarRasterParameters()
        y = StarRasterParameters()
        assert x == y

        non_defaults = dict(
            row_length_arcsec=1.0, n_rows=2, row_offset_angle=1.0, unidirectional=True
        )
        for k, v in non_defaults.items():
            y = StarRasterParameters()
            setattr(y, k, v)
            assert y != x

    def test_not_eq_to_other_objects(self):
        x = StarRasterParameters()
        y = RasterParameters()
        assert x != y

    def test_repr(self):
        x = StarRasterParameters()
        assert repr(x) == "<StarRasterParameters(0.0, 1, 0.0, False)>"


class TestPointingPattern:
    def test_defaults(self):
        x = PointingPattern()
        y = PointingPattern(
            active=SinglePointParameters.kind, parameters=[SinglePointParameters()]
        )

        assert x == y

    def test_active_parameters_must_be_contained(self):
        with pytest.raises(ValueError):
            PointingPattern(active=CrossScanParameters.kind)
        with pytest.raises(ValueError):
            PointingPattern(
                active=CrossScanParameters.kind, parameters=[SinglePointParameters()]
            )

    def test_duplicate_parameters(self):
        with pytest.raises(ValueError):
            PointingPattern(
                active=SinglePointParameters.kind,
                parameters=[SinglePointParameters(), SinglePointParameters()],
            )

    def test_eq(self):
        x = PointingPattern(
            parameters=[SinglePointParameters(), CrossScanParameters()],
            active=CrossScanParameters.kind,
        )
        other = PointingPattern(
            parameters=[SinglePointParameters(), CrossScanParameters()],
            active=CrossScanParameters.kind,
        )
        assert x == other

        # changing active should negate equality
        other = PointingPattern(
            parameters=[SinglePointParameters(), CrossScanParameters()],
            active=SinglePointParameters.kind,
        )
        assert x != other

        # but changing order should not affect equality
        other = PointingPattern(
            parameters=[CrossScanParameters(), SinglePointParameters()],
            active=CrossScanParameters.kind,
        )
        assert x == other

    def test_repr(self):
        x = PointingPattern()
        expected = f"<PointingPattern(active='SinglePointParameters', parameters=[{repr(SinglePointParameters())}])>"
        assert repr(x) == expected


class TestTarget:
    def test_defaults(self):
        expected = Target(
            target_id="",
            pointing_pattern=PointingPattern(),
            reference_coordinate=EquatorialCoordinates(),
        )
        assert Target() == expected

    def test_eq(self):
        x = Target(
            target_id="target_id",
            pointing_pattern=PointingPattern(
                active=SinglePointParameters.kind,
                parameters=[SinglePointParameters(1.0, 2.0)],
            ),
            reference_coordinate=EquatorialCoordinates(ra=1.0, dec=-0.5),
        )

        y = Target(
            target_id="target_id",
            pointing_pattern=PointingPattern(
                active=SinglePointParameters.kind,
                parameters=[SinglePointParameters(1.0, 2.0)],
            ),
            reference_coordinate=EquatorialCoordinates(ra=1.0, dec=-0.5),
        )
        assert x == y

        y = copy.deepcopy(x)
        assert x == y

        # changing target ID negates equality
        y.target_id = "foo"
        assert x != y

        y = copy.deepcopy(x)
        y.pointing_pattern = PointingPattern()
        assert x != y

        y = copy.deepcopy(x)
        y.reference_coordinate = EquatorialCoordinates()
        assert x != y

    def test_repr(self):
        target = Target("foo")
        expected = "<Target=foo | single point on 0 0>"
        assert str(target) == expected
