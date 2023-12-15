# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ska_oso_pdm.generated.models.base_model_ import Model
from ska_oso_pdm.generated import util


class CommonConfiguration(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, band_5_tuning=None, subarray_id=None):  # noqa: E501
        """CommonConfiguration - a model defined in OpenAPI

        :param band_5_tuning: The band_5_tuning of this CommonConfiguration.  # noqa: E501
        :type band_5_tuning: List[float]
        :param subarray_id: The subarray_id of this CommonConfiguration.  # noqa: E501
        :type subarray_id: int
        """
        self.openapi_types = {
            'band_5_tuning': List[float],
            'subarray_id': int
        }

        self.attribute_map = {
            'band_5_tuning': 'band_5_tuning',
            'subarray_id': 'subarray_id'
        }

        self._band_5_tuning = band_5_tuning
        self._subarray_id = subarray_id

    @classmethod
    def from_dict(cls, dikt) -> 'CommonConfiguration':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The CommonConfiguration of this CommonConfiguration.  # noqa: E501
        :rtype: CommonConfiguration
        """
        return util.deserialize_model(dikt, cls)

    @property
    def band_5_tuning(self):
        """Gets the band_5_tuning of this CommonConfiguration.


        :return: The band_5_tuning of this CommonConfiguration.
        :rtype: List[float]
        """
        return self._band_5_tuning

    @band_5_tuning.setter
    def band_5_tuning(self, band_5_tuning):
        """Sets the band_5_tuning of this CommonConfiguration.


        :param band_5_tuning: The band_5_tuning of this CommonConfiguration.
        :type band_5_tuning: List[float]
        """

        self._band_5_tuning = band_5_tuning

    @property
    def subarray_id(self):
        """Gets the subarray_id of this CommonConfiguration.


        :return: The subarray_id of this CommonConfiguration.
        :rtype: int
        """
        return self._subarray_id

    @subarray_id.setter
    def subarray_id(self, subarray_id):
        """Sets the subarray_id of this CommonConfiguration.


        :param subarray_id: The subarray_id of this CommonConfiguration.
        :type subarray_id: int
        """
        if subarray_id is None:
            raise ValueError("Invalid value for `subarray_id`, must not be `None`")  # noqa: E501

        self._subarray_id = subarray_id
