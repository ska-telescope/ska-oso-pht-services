"""
The entities.dish_configuration module defines
simple Python representation of how SKA MID dishes in sub-array should be configured.
"""
from enum import Enum

__all__ = ["DishConfigurationID", "ReceiverBand", "DishConfiguration"]

# aliases to str for entity IDs
DishConfigurationID = str


class ReceiverBand(Enum):
    """
    ReceiverBand is an enumeration of SKA MID receiver bands.
    """

    BAND_1 = "1"
    BAND_2 = "2"
    BAND_5A = "5a"
    BAND_5B = "5b"


class DishConfiguration:  # pylint: disable=too-few-public-methods
    """
    DishConfiguration specifies how SKA MID dishes in a sub-array should be
    configured. At the moment, this is limited to setting the receiver band.
    """

    def __init__(
        self, dish_configuration_id: DishConfigurationID, receiver_band: ReceiverBand
    ):
        self.dish_configuration_id = dish_configuration_id
        self.receiver_band = receiver_band

    def __eq__(self, other):
        if not isinstance(other, DishConfiguration):
            return False
        return (
            self.receiver_band == other.receiver_band
            and self.dish_configuration_id == other.dish_configuration_id
        )

    def __repr__(self):
        return (
            f"<DishConfiguration("
            f"dish_configuration_id={self.dish_configuration_id}, "
            f"receiver_band={self.receiver_band})>"
        )
