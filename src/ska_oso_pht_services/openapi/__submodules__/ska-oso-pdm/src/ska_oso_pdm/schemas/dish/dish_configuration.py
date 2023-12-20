"""
The schemas.dish_configuration_schema defines a Marshmallow schema that maps
SKA MID dishes  to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField

from ska_oso_pdm.entities.dish.dish_configuration import DishConfiguration, ReceiverBand

__all__ = ["DishConfigurationSchema"]


class DishConfigurationSchema(Schema):
    """
    The dish configuration schema section of an SKA scheduling block
    """

    dish_configuration_id = fields.String(
        required=True, data_key="dish_configuration_id"
    )

    receiver_band = EnumField(
        ReceiverBand,
        dump_by=EnumField.VALUE,
        load_by=EnumField.VALUE,
        required=True,
        data_key="receiver_band",
        error="{input} not a valid ReceiverBand. Must be one of: {values}",
    )

    @post_load
    def create_scan_definition(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a DishConfiguration

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: DishConfiguration instance populated to match JSON
        """
        return DishConfiguration(**data)
