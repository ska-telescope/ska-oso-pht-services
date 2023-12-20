"""
The schemas.sdp.scan_type module defines Marshmallow schemas .
"""
from marshmallow import Schema, fields, post_load

from ska_oso_pdm.entities.sdp import Channel, ScanType

__all__ = ["ChannelSchema", "ScanTypeSchema"]


class ChannelSchema(Schema):
    """
    Marshmallow schema for the Channel class.
    """

    count = fields.Integer(data_key="count", required=True)
    start = fields.Integer(data_key="start", required=True)
    stride = fields.Integer(data_key="stride", required=True)
    freq_min = fields.Float(data_key="freq_min", required=True)
    freq_max = fields.Float(data_key="freq_max", required=True)
    link_map = fields.List(
        fields.Tuple((fields.Integer, fields.Integer)),
        data_key="link_map",
        required=True,
    )

    @post_load
    def create_channel(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a Channel object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SubBand object populated from data
        """
        count = data["count"]
        start = data["start"]
        stride = data["stride"]
        freq_min = data["freq_min"]
        freq_max = data["freq_max"]
        link_map = data["link_map"]
        return Channel(count, start, stride, freq_min, freq_max, link_map)


class ScanTypeSchema(Schema):
    """
    Marshmallow schema for the ScanType class.
    """

    scan_type_id = fields.String(data_key="scan_type_id", required=True)
    target_id = fields.String(data_key="target", required=True)
    channels = fields.Nested(ChannelSchema, data_key="channels", many=True)

    @post_load
    def create_scan_type(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ScanType object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ScanType object populated from data
        """
        scan_type_id = data["scan_type_id"]
        target_id = data["target_id"]
        channels = data["channels"]
        return ScanType(scan_type_id, target_id, channels)
