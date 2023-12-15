# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ska_oso_pdm.generated.models.base_model_ import Model
from ska_oso_pdm.generated import util


class SubarrayConfiguration(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, subarray_name=None):  # noqa: E501
        """SubarrayConfiguration - a model defined in OpenAPI

        :param subarray_name: The subarray_name of this SubarrayConfiguration.  # noqa: E501
        :type subarray_name: str
        """
        self.openapi_types = {
            'subarray_name': str
        }

        self.attribute_map = {
            'subarray_name': 'subarray_name'
        }

        self._subarray_name = subarray_name

    @classmethod
    def from_dict(cls, dikt) -> 'SubarrayConfiguration':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SubarrayConfiguration of this SubarrayConfiguration.  # noqa: E501
        :rtype: SubarrayConfiguration
        """
        return util.deserialize_model(dikt, cls)

    @property
    def subarray_name(self):
        """Gets the subarray_name of this SubarrayConfiguration.


        :return: The subarray_name of this SubarrayConfiguration.
        :rtype: str
        """
        return self._subarray_name

    @subarray_name.setter
    def subarray_name(self, subarray_name):
        """Sets the subarray_name of this SubarrayConfiguration.


        :param subarray_name: The subarray_name of this SubarrayConfiguration.
        :type subarray_name: str
        """
        if subarray_name is None:
            raise ValueError("Invalid value for `subarray_name`, must not be `None`")  # noqa: E501

        self._subarray_name = subarray_name
