# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ska_oso_pdm.generated.models.base_model_ import Model
from ska_oso_pdm.generated import util


class SubarrayBeamConfiguration(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, update_rate=None, antenna_weights=None, phase_centre=None, subarray_beam_configuration_id=None, subarray_beam_id=None, channels=None):  # noqa: E501
        """SubarrayBeamConfiguration - a model defined in OpenAPI

        :param update_rate: The update_rate of this SubarrayBeamConfiguration.  # noqa: E501
        :type update_rate: float
        :param antenna_weights: The antenna_weights of this SubarrayBeamConfiguration.  # noqa: E501
        :type antenna_weights: List[float]
        :param phase_centre: The phase_centre of this SubarrayBeamConfiguration.  # noqa: E501
        :type phase_centre: List[float]
        :param subarray_beam_configuration_id: The subarray_beam_configuration_id of this SubarrayBeamConfiguration.  # noqa: E501
        :type subarray_beam_configuration_id: str
        :param subarray_beam_id: The subarray_beam_id of this SubarrayBeamConfiguration.  # noqa: E501
        :type subarray_beam_id: str
        :param channels: The channels of this SubarrayBeamConfiguration.  # noqa: E501
        :type channels: List[List[int]]
        """
        self.openapi_types = {
            'update_rate': float,
            'antenna_weights': List[float],
            'phase_centre': List[float],
            'subarray_beam_configuration_id': str,
            'subarray_beam_id': str,
            'channels': List[List[int]]
        }

        self.attribute_map = {
            'update_rate': 'update_rate',
            'antenna_weights': 'antenna_weights',
            'phase_centre': 'phase_centre',
            'subarray_beam_configuration_id': 'subarray_beam_configuration_id',
            'subarray_beam_id': 'subarray_beam_id',
            'channels': 'channels'
        }

        self._update_rate = update_rate
        self._antenna_weights = antenna_weights
        self._phase_centre = phase_centre
        self._subarray_beam_configuration_id = subarray_beam_configuration_id
        self._subarray_beam_id = subarray_beam_id
        self._channels = channels

    @classmethod
    def from_dict(cls, dikt) -> 'SubarrayBeamConfiguration':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SubarrayBeamConfiguration of this SubarrayBeamConfiguration.  # noqa: E501
        :rtype: SubarrayBeamConfiguration
        """
        return util.deserialize_model(dikt, cls)

    @property
    def update_rate(self):
        """Gets the update_rate of this SubarrayBeamConfiguration.


        :return: The update_rate of this SubarrayBeamConfiguration.
        :rtype: float
        """
        return self._update_rate

    @update_rate.setter
    def update_rate(self, update_rate):
        """Sets the update_rate of this SubarrayBeamConfiguration.


        :param update_rate: The update_rate of this SubarrayBeamConfiguration.
        :type update_rate: float
        """
        if update_rate is None:
            raise ValueError("Invalid value for `update_rate`, must not be `None`")  # noqa: E501

        self._update_rate = update_rate

    @property
    def antenna_weights(self):
        """Gets the antenna_weights of this SubarrayBeamConfiguration.


        :return: The antenna_weights of this SubarrayBeamConfiguration.
        :rtype: List[float]
        """
        return self._antenna_weights

    @antenna_weights.setter
    def antenna_weights(self, antenna_weights):
        """Sets the antenna_weights of this SubarrayBeamConfiguration.


        :param antenna_weights: The antenna_weights of this SubarrayBeamConfiguration.
        :type antenna_weights: List[float]
        """
        if antenna_weights is None:
            raise ValueError("Invalid value for `antenna_weights`, must not be `None`")  # noqa: E501

        self._antenna_weights = antenna_weights

    @property
    def phase_centre(self):
        """Gets the phase_centre of this SubarrayBeamConfiguration.


        :return: The phase_centre of this SubarrayBeamConfiguration.
        :rtype: List[float]
        """
        return self._phase_centre

    @phase_centre.setter
    def phase_centre(self, phase_centre):
        """Sets the phase_centre of this SubarrayBeamConfiguration.


        :param phase_centre: The phase_centre of this SubarrayBeamConfiguration.
        :type phase_centre: List[float]
        """
        if phase_centre is None:
            raise ValueError("Invalid value for `phase_centre`, must not be `None`")  # noqa: E501

        self._phase_centre = phase_centre

    @property
    def subarray_beam_configuration_id(self):
        """Gets the subarray_beam_configuration_id of this SubarrayBeamConfiguration.


        :return: The subarray_beam_configuration_id of this SubarrayBeamConfiguration.
        :rtype: str
        """
        return self._subarray_beam_configuration_id

    @subarray_beam_configuration_id.setter
    def subarray_beam_configuration_id(self, subarray_beam_configuration_id):
        """Sets the subarray_beam_configuration_id of this SubarrayBeamConfiguration.


        :param subarray_beam_configuration_id: The subarray_beam_configuration_id of this SubarrayBeamConfiguration.
        :type subarray_beam_configuration_id: str
        """
        if subarray_beam_configuration_id is None:
            raise ValueError("Invalid value for `subarray_beam_configuration_id`, must not be `None`")  # noqa: E501

        self._subarray_beam_configuration_id = subarray_beam_configuration_id

    @property
    def subarray_beam_id(self):
        """Gets the subarray_beam_id of this SubarrayBeamConfiguration.


        :return: The subarray_beam_id of this SubarrayBeamConfiguration.
        :rtype: str
        """
        return self._subarray_beam_id

    @subarray_beam_id.setter
    def subarray_beam_id(self, subarray_beam_id):
        """Sets the subarray_beam_id of this SubarrayBeamConfiguration.


        :param subarray_beam_id: The subarray_beam_id of this SubarrayBeamConfiguration.
        :type subarray_beam_id: str
        """
        if subarray_beam_id is None:
            raise ValueError("Invalid value for `subarray_beam_id`, must not be `None`")  # noqa: E501

        self._subarray_beam_id = subarray_beam_id

    @property
    def channels(self):
        """Gets the channels of this SubarrayBeamConfiguration.


        :return: The channels of this SubarrayBeamConfiguration.
        :rtype: List[List[int]]
        """
        return self._channels

    @channels.setter
    def channels(self, channels):
        """Sets the channels of this SubarrayBeamConfiguration.


        :param channels: The channels of this SubarrayBeamConfiguration.
        :type channels: List[List[int]]
        """
        if channels is None:
            raise ValueError("Invalid value for `channels`, must not be `None`")  # noqa: E501

        self._channels = channels
