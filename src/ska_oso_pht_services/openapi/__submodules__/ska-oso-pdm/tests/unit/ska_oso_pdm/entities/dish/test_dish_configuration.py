"""
Unit tests for the ska_oso_pdm.entities.dish_configuration module.
"""

from ska_oso_pdm.entities.dish.dish_configuration import DishConfiguration, ReceiverBand


def test_dish_configuration_eq():
    """
    Verify that DishConfiguration objects are considered equal when:
      - they use the same receiver band and the same id
    """
    id_1 = "config 1"
    id_2 = "config 2"

    config_1 = DishConfiguration(id_1, receiver_band=ReceiverBand.BAND_1)
    config_2 = DishConfiguration(id_1, receiver_band=ReceiverBand.BAND_1)
    config_3 = DishConfiguration(id_2, receiver_band=ReceiverBand.BAND_1)
    config_4 = DishConfiguration(id_1, receiver_band=ReceiverBand.BAND_2)
    config_5 = DishConfiguration(id_2, receiver_band=ReceiverBand.BAND_2)

    assert config_1 == config_2
    assert config_1 != config_3
    assert config_1 != config_4
    assert config_1 != config_5


def test_dish_configuration_is_not_equal_to_other_objects():
    """
    Verify that DishConfiguration is considered unequal to
    non-DishConfiguration objects.
    :return:
    """
    id_1 = "config 1"
    config_1 = DishConfiguration(id_1, receiver_band=ReceiverBand.BAND_1)
    assert config_1 != object
