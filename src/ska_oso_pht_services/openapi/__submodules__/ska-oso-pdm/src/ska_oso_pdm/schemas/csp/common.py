"""
The schemas.csp_schema defines Marshmallow schemas that map the CSP
definition section of an SKA scheduling block to/from JSON.
"""
from marshmallow import Schema, fields, post_dump, post_load
from marshmallow_enum import EnumField

from ska_oso_pdm.entities.csp import common as csp_entities

__all__ = [
    "CSPConfigurationSchema",
    "FSPConfigurationSchema",
    "SubarrayConfigurationSchema",
    "CommonConfigurationSchema",
    "CBFConfigurationSchema",
]


class SubarrayConfigurationSchema(Schema):
    """
    Marshmallow schema for the SubarrayConfigurationSchema
    """

    subarray_name = fields.String(data_key="subarray_name", required=True)

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a SubarrayConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: SubarrayConfiguration instance populated to match JSON
        :rtype: SubarrayConfiguration
        """
        subarray_name = data["subarray_name"]
        return csp_entities.SubarrayConfiguration(subarray_name)


class CommonConfigurationSchema(Schema):
    """
    Marshmallow schema for the CommonConfigurationSchema
    """

    subarray_id = fields.Integer(data_key="subarray_id", required=True)
    band_5_tuning = fields.List(fields.Float, data_key="band_5_tuning")

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a CSPConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: CommonConfiguration instance populated to match JSON
        """
        subarray_id = data.get("subarray_id", None)
        band_5_tuning = data.get("band_5_tuning", None)

        return csp_entities.CommonConfiguration(subarray_id, band_5_tuning)

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for FSP configuration
        """
        result = {k: v for k, v in data.items() if v is not None}
        return result


class FSPConfigurationSchema(Schema):
    """
    Marshmallow schema for the FSPConfiguration
    """

    fsp_id = fields.Integer(data_key="fsp_id", required=True)

    function_mode = EnumField(
        csp_entities.FSPFunctionMode,
        dump_by=EnumField.VALUE,
        load_by=EnumField.VALUE,
        required=True,
        data_key="function_mode",
        error="{input} not a valid FSPFunctionMode. Must be one of: {values}",
    )

    frequency_slice_id = fields.Integer(data_key="frequency_slice_id", required=True)
    zoom_factor = fields.Integer(data_key="zoom_factor", required=True)
    integration_factor = fields.Integer(data_key="integration_factor", required=True)
    channel_averaging_map = fields.List(
        fields.Tuple((fields.Integer, fields.Integer)), data_key="channel_averaging_map"
    )
    output_link_map = fields.List(
        fields.Tuple((fields.Integer, fields.Integer)), data_key="output_link_map"
    )
    channel_offset = fields.Integer(data_key="channel_offset")
    zoom_window_tuning = fields.Integer(data_key="zoom_window_tuning")

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for FSP configuration
        """
        result = {k: v for k, v in data.items() if v is not None}
        return result

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a FSPConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: FSPConfiguration instance populated to match JSON

        """
        fsp_id = data["fsp_id"]
        function_mode = data["function_mode"]
        frequency_slice_id = int(data["frequency_slice_id"])
        zoom_factor = data["zoom_factor"]
        integration_factor = data["integration_factor"]

        # optional arguments
        channel_averaging_map = data.get("channel_averaging_map", None)
        output_link_map = data.get("output_link_map", None)
        channel_offset = data.get("channel_offset", None)
        zoom_window_tuning = data.get("zoom_window_tuning", None)

        return csp_entities.FSPConfiguration(
            fsp_id,
            function_mode,
            frequency_slice_id,
            integration_factor,
            zoom_factor,
            channel_averaging_map=channel_averaging_map,
            output_link_map=output_link_map,
            channel_offset=channel_offset,
            zoom_window_tuning=zoom_window_tuning,
        )


class CBFConfigurationSchema(Schema):
    """
    Marshmallow schema for the CBFConfigurationSchema
    """

    fsp_configs = fields.Nested(FSPConfigurationSchema, many=True, data_key="fsp")

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
         Convert parsed JSON back into a CBFConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: CBFConfiguration instance populated to match JSON
        :rtype: CBFConfiguration
        """
        fsp_configs = data["fsp_configs"]
        return csp_entities.CBFConfiguration(fsp_configs)


class CSPConfigurationSchema(Schema):
    """
    Marshmallow schema for the ska_oso_pdm.CSPConfiguration class
    """

    config_id = fields.String(data_key="config_id")
    subarray_config = fields.Nested(SubarrayConfigurationSchema, data_key="subarray")
    common_config = fields.Nested(CommonConfigurationSchema, data_key="common")
    cbf_config = fields.Nested(CBFConfigurationSchema, data_key="cbf")

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a CSPConfiguration object.

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: CSPConfiguration instance populated to match JSON

        """
        config_id = data.get("config_id", None)
        subarray_config = data.get("subarray_config", None)
        common_config = data.get("common_config", None)
        cbf_config = data.get("cbf_config", None)

        return csp_entities.CSPConfiguration(
            config_id, subarray_config, common_config, cbf_config
        )

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for SubArrayNode configuration
        """
        return {k: v for k, v in data.items() if v is not None}
