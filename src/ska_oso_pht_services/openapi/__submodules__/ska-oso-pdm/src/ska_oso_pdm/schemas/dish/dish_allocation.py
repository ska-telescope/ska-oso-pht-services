"""
The schemas.dish_allocation module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_load

from ska_oso_pdm.entities.dish.dish_allocation import DishAllocation

__all__ = ["DishAllocationSchema"]


class DishAllocationSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the DishAllocation class.
    """

    receptor_ids = fields.List(
        fields.String, data_key="receptor_ids", many=True, required=True
    )

    @post_load
    def create(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a DishAllocation object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: DishAllocation object populated from data
        """
        receptor_ids = data["receptor_ids"]
        return DishAllocation(receptor_ids=receptor_ids)
