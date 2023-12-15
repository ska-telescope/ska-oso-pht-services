"""
tests for the dish_configuration_schema to validate the
conversion between the JSON and Python representations
of an SKA Scheduling Block
"""
from ska_oso_pdm.entities.dish.dish_configuration import DishConfiguration, ReceiverBand
from ska_oso_pdm.schemas.dish.dish_configuration import DishConfigurationSchema
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal

VALID_DISH_CONFIGURATION_JSON = (
    '{"dish_configuration_id": "dish config 123", "receiver_band": "5a"}'
)


def test_marshall_dish_configuration_to_json():
    """
    Verify that DishConfiguration is marshalled to JSON correctly.
    """

    config = DishConfiguration("dish config 123", receiver_band=ReceiverBand.BAND_5A)
    json_str = DishConfigurationSchema().dumps(config)
    assert_json_is_equal(json_str, VALID_DISH_CONFIGURATION_JSON)


def test_unmarshall_dish_configuration_from_json():
    """
    Verify that JSON can be unmarshalled to a DishConfiguration
    """

    expected = DishConfiguration("dish config 123", receiver_band=ReceiverBand.BAND_5A)
    unmarshalled = DishConfigurationSchema().loads(VALID_DISH_CONFIGURATION_JSON)
    assert unmarshalled == expected
