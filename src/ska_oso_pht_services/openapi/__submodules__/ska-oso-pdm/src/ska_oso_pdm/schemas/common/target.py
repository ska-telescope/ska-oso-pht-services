"""
The schemas.common.target defines Marshmallow schema that map the
target pointing section of an SKA scheduling block to/from JSON.
"""
import collections

from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from marshmallow_oneofschema import OneOfSchema

from ...entities.common.target import (
    Coordinates,
    CrossScanParameters,
    EquatorialCoordinates,
    EquatorialCoordinatesReferenceFrame,
    FivePointParameters,
    HorizontalCoordinates,
    HorizontalCoordinatesReferenceFrame,
    PointingPattern,
    PointingPatternParameters,
    RasterParameters,
    SinglePointParameters,
    SolarSystemObject,
    SolarSystemObjectName,
    StarRasterParameters,
    Target,
)


class SolarSystemObjectSchema(Schema):
    """
    Schema for marshalling SolarSystemObject coordinates to/from JSON
    """

    # For Planet the name is an enum, however in the parent
    # Target class (which the schema uses) it is a string
    # For this reason the target_name is not handled with the
    # marshmallow_enum.EnumField like other enums
    kind = fields.String(required=True)
    name = EnumField(
        SolarSystemObjectName,
        dump_by=EnumField.VALUE,
        load_by=EnumField.VALUE,
        required=True,
        error="Must be one of: {values}",
    )

    @post_load
    def create_instance(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a SolarSystemObject

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: instance populated to match JSON
        """
        return SolarSystemObject(name=data["name"])


JsonEquatorialCoordinate = collections.namedtuple(
    "JsonEquatorialCoordinate", "kind ra dec reference_frame unit"
)

JsonHorizontalCoordinate = collections.namedtuple(
    "JsonHorizontalCoordinate", "kind az el reference_frame unit"
)


class EquatorialCoordinatesSchema(Schema):
    """
    Convert an EquatorialCoordinates to/from JSON.
    """

    kind = fields.String(required=True)
    ra = fields.String(required=True)
    dec = fields.String(required=True)
    reference_frame = EnumField(
        EquatorialCoordinatesReferenceFrame,
        dump_by=EnumField.NAME,
        load_by=EnumField.NAME,
        required=True,
        error="{input} not a valid reference frame. Must be one of: {values}",
    )
    unit = fields.List(fields.String(), required=True)

    @post_load
    def make_equatorialcoordinates(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into an EquatorialCoordinates object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: EquatorialCoordinates instance populated to match JSON
        """
        coords = EquatorialCoordinates(
            ra=data["ra"],
            dec=data["dec"],
            reference_frame=data["reference_frame"],
            unit=data["unit"],
        )
        return coords


class HorizontalCoordinatesSchema(Schema):
    """
    Marshmallow schema to convert a HorizontalCoordinates to/from JSON.
    """

    kind = fields.String(required=True)
    az = fields.Float(required=True)
    el = fields.Float(required=True)
    unit = fields.List(fields.String(), required=True)
    reference_frame = EnumField(
        HorizontalCoordinatesReferenceFrame,
        dump_by=EnumField.NAME,
        load_by=EnumField.NAME,
        required=True,
        error="{input} not a valid reference frame. Must be one of: {values}",
    )

    @post_load
    def make_horizontalcoordinates(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a HorizontalCoordinates object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: HorizontalCoordinates instance populated to match JSON
        """
        return HorizontalCoordinates(
            az=data["az"],
            el=data["el"],
            unit=data["unit"],
        )


class CoordinatesSchema(OneOfSchema):
    """
    Marshmallow schema for handling polymorphic coordinates classes.
    """

    type_field = "kind"
    # kind is a required field of the implementing subclasses so do not remove it
    type_field_remove = False
    type_schemas = {
        EquatorialCoordinates.kind: EquatorialCoordinatesSchema,
        HorizontalCoordinates.kind: HorizontalCoordinatesSchema,
        SolarSystemObject.kind: SolarSystemObjectSchema,
    }

    def get_obj_type(self, obj):
        if isinstance(obj, Coordinates):
            return obj.kind

        raise Exception(f"Unknown object type: {obj.__class__.__name__}")


class CrossScanParametersSchema(Schema):
    """
    Marshmallow schema for converting a CrossScanParameters to/from JSON
    """

    offset_arcsec = fields.Float(required=True)
    kind = fields.String(required=True)

    @post_load
    def make_crossscanparameters(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a CrossScanParameters object

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: CrossScanParameters instance populated to match JSON
        """
        offset_arcsec = data["offset_arcsec"]
        return CrossScanParameters(offset_arcsec=offset_arcsec)


class FivePointParametersSchema(Schema):
    """
    Marshmallow schema for converting a FivePointParameters to/from JSON
    """

    offset_arcsec = fields.Float(required=True)
    kind = fields.String(required=True)

    @post_load
    def make_fivepointparameters(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a FivePointParameters object

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: FivePointParameters instance populated to match JSON
        """
        offset_arcsec = data["offset_arcsec"]
        return FivePointParameters(offset_arcsec=offset_arcsec)


class SinglePointParametersSchema(Schema):
    """
    Marshmallow schema for converting a SinglePointParameters to/from JSON
    """

    offset_x_arcsec = fields.Float(required=True)
    offset_y_arcsec = fields.Float(required=True)
    kind = fields.String(required=True)

    @post_load
    def make_singlepointparameters(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a SinglePointParameters object

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SinglePointParameters instance populated to match JSON
        """
        offset_x_arcsec = data["offset_x_arcsec"]
        offset_y_arcsec = data["offset_y_arcsec"]
        return SinglePointParameters(
            offset_x_arcsec=offset_x_arcsec, offset_y_arcsec=offset_y_arcsec
        )


class RasterParametersSchema(Schema):
    """
    Marshmallow schema for converting a RasterParameters to/from JSON
    """

    kind = fields.String(required=True)
    row_length_arcsec = fields.Float(default=0.0, required=True)
    row_offset_arcsec = fields.Float(default=0.0, required=True)
    n_rows = fields.Integer(default=1, required=True)
    pa = fields.Float(default=0.0, required=True)
    unidirectional = fields.Bool(default=False, required=True)

    @post_load
    def make_rasterparameters(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a RasterParameters object

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: RasterParameters instance populated to match JSON
        """
        return RasterParameters(
            row_length_arcsec=data["row_length_arcsec"],
            row_offset_arcsec=data["row_offset_arcsec"],
            n_rows=data["n_rows"],
            pa=data["pa"],
            unidirectional=data["unidirectional"],
        )


class StarRasterParametersSchema(Schema):
    """
    Marshmallow schema for converting a StarRasterParameters to/from JSON
    """

    kind = fields.String(required=True)
    row_length_arcsec = fields.Float(default=0.0, required=True)
    n_rows = fields.Integer(default=1, required=True)
    row_offset_angle = fields.Float(default=0.0, required=True)
    unidirectional = fields.Bool(default=False, required=True)

    @post_load
    def make_starrasterparameters(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a StarRasterParameters object

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: StarRasterParameters instance populated to match JSON
        """
        return StarRasterParameters(
            row_length_arcsec=data["row_length_arcsec"],
            n_rows=data["n_rows"],
            row_offset_angle=data["row_offset_angle"],
            unidirectional=data["unidirectional"],
        )


class PointingPatternParametersSchema(OneOfSchema):
    """
    Marshmallow schema for handling polymorphic pointing pattern parameter classes.
    """

    type_field = "kind"
    # kind is a required field of the implementing subclasses so do not remove it
    type_field_remove = False
    type_schemas = {
        SinglePointParameters.kind: SinglePointParametersSchema,
        FivePointParameters.kind: FivePointParametersSchema,
        CrossScanParameters.kind: CrossScanParametersSchema,
        RasterParameters.kind: RasterParametersSchema,
        StarRasterParameters.kind: StarRasterParametersSchema,
    }

    def get_obj_type(self, obj):
        if isinstance(obj, PointingPatternParameters):
            return obj.kind

        raise Exception(f"Unknown object type: {obj.__class__.__name__}")


class PointingPatternSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshallow schema for converts a PointingPattern to/from JSON.
    """

    active = fields.String(required=True)
    parameters = fields.List(fields.Nested(PointingPatternParametersSchema))

    @post_load
    def make_pointingpattern(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a PointingPattern object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: PointingPattern instance populated to match JSON

        """
        active = data.get("active")
        parameters = data.get("parameters")
        return PointingPattern(active=active, parameters=parameters)


class TargetSchema(Schema):
    """
    Marshmallow class to convert Target to/from JSON.
    """

    target_id = fields.String(required=True)
    pointing_pattern = fields.Nested(PointingPatternSchema, required=True)
    reference_coordinate = fields.Nested(CoordinatesSchema, required=True)

    @post_load
    def make_target(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a Target object

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: Target instance populated to match JSON
        """
        return Target(
            target_id=data["target_id"],
            pointing_pattern=data["pointing_pattern"],
            reference_coordinate=data["reference_coordinate"],
        )
