# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ska_oso_pdm.generated.models.base_model_ import Model
from ska_oso_pdm.generated.models.horizontal_coordinates_reference_frame import HorizontalCoordinatesReferenceFrame
from ska_oso_pdm.generated import util

from ska_oso_pdm.generated.models.horizontal_coordinates_reference_frame import HorizontalCoordinatesReferenceFrame  # noqa: E501

class HorizontalCoordinatesAllOf(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, az=None, el=None, reference_frame=None, unit=None):  # noqa: E501
        """HorizontalCoordinatesAllOf - a model defined in OpenAPI

        :param az: The az of this HorizontalCoordinatesAllOf.  # noqa: E501
        :type az: float
        :param el: The el of this HorizontalCoordinatesAllOf.  # noqa: E501
        :type el: float
        :param reference_frame: The reference_frame of this HorizontalCoordinatesAllOf.  # noqa: E501
        :type reference_frame: HorizontalCoordinatesReferenceFrame
        :param unit: The unit of this HorizontalCoordinatesAllOf.  # noqa: E501
        :type unit: List[str]
        """
        self.openapi_types = {
            'az': float,
            'el': float,
            'reference_frame': HorizontalCoordinatesReferenceFrame,
            'unit': List[str]
        }

        self.attribute_map = {
            'az': 'az',
            'el': 'el',
            'reference_frame': 'reference_frame',
            'unit': 'unit'
        }

        self._az = az
        self._el = el
        self._reference_frame = reference_frame
        self._unit = unit

    @classmethod
    def from_dict(cls, dikt) -> 'HorizontalCoordinatesAllOf':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The HorizontalCoordinates_allOf of this HorizontalCoordinatesAllOf.  # noqa: E501
        :rtype: HorizontalCoordinatesAllOf
        """
        return util.deserialize_model(dikt, cls)

    @property
    def az(self):
        """Gets the az of this HorizontalCoordinatesAllOf.


        :return: The az of this HorizontalCoordinatesAllOf.
        :rtype: float
        """
        return self._az

    @az.setter
    def az(self, az):
        """Sets the az of this HorizontalCoordinatesAllOf.


        :param az: The az of this HorizontalCoordinatesAllOf.
        :type az: float
        """
        if az is None:
            raise ValueError("Invalid value for `az`, must not be `None`")  # noqa: E501

        self._az = az

    @property
    def el(self):
        """Gets the el of this HorizontalCoordinatesAllOf.


        :return: The el of this HorizontalCoordinatesAllOf.
        :rtype: float
        """
        return self._el

    @el.setter
    def el(self, el):
        """Sets the el of this HorizontalCoordinatesAllOf.


        :param el: The el of this HorizontalCoordinatesAllOf.
        :type el: float
        """
        if el is None:
            raise ValueError("Invalid value for `el`, must not be `None`")  # noqa: E501

        self._el = el

    @property
    def reference_frame(self):
        """Gets the reference_frame of this HorizontalCoordinatesAllOf.


        :return: The reference_frame of this HorizontalCoordinatesAllOf.
        :rtype: HorizontalCoordinatesReferenceFrame
        """
        return self._reference_frame

    @reference_frame.setter
    def reference_frame(self, reference_frame):
        """Sets the reference_frame of this HorizontalCoordinatesAllOf.


        :param reference_frame: The reference_frame of this HorizontalCoordinatesAllOf.
        :type reference_frame: HorizontalCoordinatesReferenceFrame
        """
        if reference_frame is None:
            raise ValueError("Invalid value for `reference_frame`, must not be `None`")  # noqa: E501

        self._reference_frame = reference_frame

    @property
    def unit(self):
        """Gets the unit of this HorizontalCoordinatesAllOf.


        :return: The unit of this HorizontalCoordinatesAllOf.
        :rtype: List[str]
        """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """Sets the unit of this HorizontalCoordinatesAllOf.


        :param unit: The unit of this HorizontalCoordinatesAllOf.
        :type unit: List[str]
        """
        if unit is None:
            raise ValueError("Invalid value for `unit`, must not be `None`")  # noqa: E501

        self._unit = unit
