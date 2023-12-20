"""
tests for the target schema to validate the
conversion between the JSON and Python representations
of the field configuration section of an SKA Scheduling Block
"""
import pytest
from marshmallow.exceptions import ValidationError

from ska_oso_pdm.entities.common.target import (
    CrossScanParameters,
    EquatorialCoordinates,
    FivePointParameters,
    HorizontalCoordinates,
    PointingPattern,
    RasterParameters,
    SinglePointParameters,
    SolarSystemObject,
    SolarSystemObjectName,
    StarRasterParameters,
    Target,
)
from ska_oso_pdm.schemas.common.target import (
    CoordinatesSchema,
    CrossScanParametersSchema,
    EquatorialCoordinatesSchema,
    FivePointParametersSchema,
    HorizontalCoordinatesSchema,
    PointingPatternParametersSchema,
    PointingPatternSchema,
    RasterParametersSchema,
    SinglePointParametersSchema,
    SolarSystemObjectSchema,
    StarRasterParametersSchema,
    TargetSchema,
)
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal


class TestCrossScanParametersSchema:
    VALID_JSON = """{
    "kind": "CrossScanParameters",
    "offset_arcsec": 1.23
}"""

    VALID_OBJECT = CrossScanParameters(1.23)

    def test_marshal(self):
        json_str = CrossScanParametersSchema().dumps(self.VALID_OBJECT)
        assert_json_is_equal(json_str, self.VALID_JSON)

    def test_unmarshal(self):
        unmarshalled = CrossScanParametersSchema().loads(self.VALID_JSON)
        assert unmarshalled == self.VALID_OBJECT


class TestFivePointParametersSchema:
    VALID_JSON = """{
    "kind": "FivePointParameters",
    "offset_arcsec": 1.23
}"""

    VALID_OBJECT = FivePointParameters(1.23)

    def test_marshal(self):
        json_str = FivePointParametersSchema().dumps(self.VALID_OBJECT)
        assert_json_is_equal(json_str, self.VALID_JSON)

    def test_unmarshal(self):
        unmarshalled = FivePointParametersSchema().loads(self.VALID_JSON)
        assert unmarshalled == self.VALID_OBJECT


class TestSinglePointParametersSchema:
    VALID_JSON = """{
    "kind": "SinglePointParameters",
    "offset_x_arcsec": 1.23,
    "offset_y_arcsec": 4.56
}"""

    VALID_OBJECT = SinglePointParameters(1.23, 4.56)

    def test_marshal(self):
        json_str = SinglePointParametersSchema().dumps(self.VALID_OBJECT)
        assert_json_is_equal(json_str, self.VALID_JSON)

    def test_unmarshal(self):
        unmarshalled = SinglePointParametersSchema().loads(self.VALID_JSON)
        assert unmarshalled == self.VALID_OBJECT


class TestRasterParametersSchema:
    VALID_JSON = """{
    "kind": "RasterParameters",
    "row_length_arcsec": 1.23,
    "row_offset_arcsec": 4.56,
    "n_rows": 2,
    "pa": 7.89,
    "unidirectional": true
}"""

    VALID_OBJECT = RasterParameters(
        row_length_arcsec=1.23,
        row_offset_arcsec=4.56,
        n_rows=2,
        pa=7.89,
        unidirectional=True,
    )

    def test_marshal(self):
        json_str = RasterParametersSchema().dumps(self.VALID_OBJECT)
        assert_json_is_equal(json_str, self.VALID_JSON)

    def test_unmarshal(self):
        unmarshalled = RasterParametersSchema().loads(self.VALID_JSON)
        assert unmarshalled == self.VALID_OBJECT


class TestStarRasterParametersSchema:
    VALID_JSON = """{
    "kind": "StarRasterParameters",
    "row_length_arcsec": 1.23,
    "n_rows": 2,
    "row_offset_angle": 4.56,
    "unidirectional": true
}"""

    VALID_OBJECT = StarRasterParameters(
        row_length_arcsec=1.23, n_rows=2, row_offset_angle=4.56, unidirectional=True
    )

    def test_marshal(self):
        json_str = StarRasterParametersSchema().dumps(self.VALID_OBJECT)
        assert_json_is_equal(json_str, self.VALID_JSON)

    def test_unmarshal(self):
        unmarshalled = StarRasterParametersSchema().loads(self.VALID_JSON)
        assert unmarshalled == self.VALID_OBJECT


class TestPointingPatternParametersSchema:
    @staticmethod
    @pytest.mark.parametrize(
        "instance,expected",
        [
            (
                TestSinglePointParametersSchema.VALID_OBJECT,
                TestSinglePointParametersSchema.VALID_JSON,
            ),
            (
                TestFivePointParametersSchema.VALID_OBJECT,
                TestFivePointParametersSchema.VALID_JSON,
            ),
            (
                TestCrossScanParametersSchema.VALID_OBJECT,
                TestCrossScanParametersSchema.VALID_JSON,
            ),
        ],
    )
    def test_marshal(instance, expected):
        json_str = PointingPatternParametersSchema().dumps(instance)
        assert_json_is_equal(json_str, expected)

    @staticmethod
    @pytest.mark.parametrize(
        "expected,json_str",
        [
            (
                TestSinglePointParametersSchema.VALID_OBJECT,
                TestSinglePointParametersSchema.VALID_JSON,
            ),
            (
                TestFivePointParametersSchema.VALID_OBJECT,
                TestFivePointParametersSchema.VALID_JSON,
            ),
            (
                TestCrossScanParametersSchema.VALID_OBJECT,
                TestCrossScanParametersSchema.VALID_JSON,
            ),
        ],
    )
    def test_unmarshal(expected, json_str):
        unmarshalled = PointingPatternParametersSchema().loads(json_str)
        assert unmarshalled == expected


class TestPointingPatternSchema:
    VALID_JSON = (
        """{
    "active": "CrossScanParameters",
    "parameters": [
    """
        + TestCrossScanParametersSchema.VALID_JSON
        + """,
    """
        + TestSinglePointParametersSchema.VALID_JSON
        + """
    ]
}"""
    )

    VALID_OBJECT = PointingPattern(
        active=CrossScanParameters.kind,
        parameters=[
            TestCrossScanParametersSchema.VALID_OBJECT,
            TestSinglePointParametersSchema.VALID_OBJECT,
        ],
    )

    def test_marshal(self):
        json_str = PointingPatternSchema().dumps(self.VALID_OBJECT)
        assert_json_is_equal(json_str, self.VALID_JSON)

    def test_unmarshal(self):
        unmarshalled = PointingPatternSchema().loads(self.VALID_JSON)
        assert unmarshalled == self.VALID_OBJECT


class TestEquatorialCoordinates:
    VALID_JSON = """{
    "kind": "equatorial",
    "ra": "12:34:56.78",
    "dec": "-12:34:56.78",
    "reference_frame": "ICRS",
    "unit": ["hourangle", "deg"]
}"""

    VALID_OBJECT = EquatorialCoordinates(
        ra="12:34:56.78",
        dec="-12:34:56.78",
    )

    def test_marshal(self):
        json_str = EquatorialCoordinatesSchema().dumps(self.VALID_OBJECT)
        assert_json_is_equal(json_str, self.VALID_JSON)

    def test_unmarshal(self):
        unmarshalled = EquatorialCoordinatesSchema().loads(self.VALID_JSON)
        assert unmarshalled == self.VALID_OBJECT


class TestHorizontalCoordinates:
    VALID_JSON = """{
    "kind": "horizontal",
    "az": 12.34,
    "el": 56.78,
    "reference_frame": "ALTAZ",
    "unit": ["deg"]
}"""

    VALID_OBJECT = HorizontalCoordinates(az=12.34, el=56.78)

    def test_marshal(self):
        json_str = HorizontalCoordinatesSchema().dumps(self.VALID_OBJECT)
        assert_json_is_equal(json_str, self.VALID_JSON)

    def test_unmarshal(self):
        unmarshalled = HorizontalCoordinatesSchema().loads(self.VALID_JSON)
        assert unmarshalled == self.VALID_OBJECT


class TestSolarSystemObject:
    VALID_JSON = """{
    "kind": "sso",
    "name": "venus"
}"""

    VALID_OBJECT = SolarSystemObject(SolarSystemObjectName.VENUS)

    def test_marshal(self):
        json_str = SolarSystemObjectSchema().dumps(self.VALID_OBJECT)
        assert_json_is_equal(json_str, self.VALID_JSON)

    def test_unmarshal(self):
        unmarshalled = SolarSystemObjectSchema().loads(self.VALID_JSON)
        assert unmarshalled == self.VALID_OBJECT

    def test_unmarshall_invalid_planet_from_json(self):
        """
        Verify that a validation error is thrown when a invalid Planet is given.
        """
        invalid_planet_json = self.VALID_JSON.replace("venus", "arrakis")
        with pytest.raises(ValidationError):
            SolarSystemObjectSchema().loads(invalid_planet_json)


class TestCoordinatesSchema:
    @staticmethod
    @pytest.mark.parametrize(
        "instance,expected",
        [
            (
                TestEquatorialCoordinates.VALID_OBJECT,
                TestEquatorialCoordinates.VALID_JSON,
            ),
            (
                TestHorizontalCoordinates.VALID_OBJECT,
                TestHorizontalCoordinates.VALID_JSON,
            ),
            (TestSolarSystemObject.VALID_OBJECT, TestSolarSystemObject.VALID_JSON),
        ],
    )
    def test_marshal(instance, expected):
        json_str = CoordinatesSchema().dumps(instance)
        assert_json_is_equal(json_str, expected)

    @staticmethod
    @pytest.mark.parametrize(
        "expected,json_str",
        [
            (
                TestEquatorialCoordinates.VALID_OBJECT,
                TestEquatorialCoordinates.VALID_JSON,
            ),
            (
                TestHorizontalCoordinates.VALID_OBJECT,
                TestHorizontalCoordinates.VALID_JSON,
            ),
            (TestSolarSystemObject.VALID_OBJECT, TestSolarSystemObject.VALID_JSON),
        ],
    )
    def test_unmarshal(expected, json_str):
        unmarshalled = CoordinatesSchema().loads(json_str)
        assert unmarshalled == expected


class TestTarget:
    VALID_JSON = (
        """{
    "target_id": "foo",
    "pointing_pattern": """
        + TestPointingPatternSchema.VALID_JSON
        + """,
    "reference_coordinate": """
        + TestEquatorialCoordinates.VALID_JSON
        + """
}"""
    )

    VALID_OBJECT = Target(
        target_id="foo",
        pointing_pattern=TestPointingPatternSchema.VALID_OBJECT,
        reference_coordinate=TestEquatorialCoordinates.VALID_OBJECT,
    )

    def test_marshal(self):
        json_str = TargetSchema().dumps(self.VALID_OBJECT)
        assert_json_is_equal(json_str, self.VALID_JSON)

    def test_unmarshal(self):
        unmarshalled = TargetSchema().loads(self.VALID_JSON)
        assert unmarshalled == self.VALID_OBJECT
