# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ska_oso_pdm.generated.models.base_model_ import Model
from ska_oso_pdm.generated.models.coordinates import Coordinates
from ska_oso_pdm.generated.models.solar_system_object_name import SolarSystemObjectName
from ska_oso_pdm.generated import util

from ska_oso_pdm.generated.models.coordinates import Coordinates  # noqa: E501
from ska_oso_pdm.generated.models.solar_system_object_name import SolarSystemObjectName  # noqa: E501

class SolarSystemObject(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, kind=None, name=None):  # noqa: E501
        """SolarSystemObject - a model defined in OpenAPI

        :param kind: The kind of this SolarSystemObject.  # noqa: E501
        :type kind: str
        :param name: The name of this SolarSystemObject.  # noqa: E501
        :type name: SolarSystemObjectName
        """
        self.openapi_types = {
            'kind': str,
            'name': SolarSystemObjectName
        }

        self.attribute_map = {
            'kind': 'kind',
            'name': 'name'
        }

        self._kind = kind
        self._name = name

    @classmethod
    def from_dict(cls, dikt) -> 'SolarSystemObject':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SolarSystemObject of this SolarSystemObject.  # noqa: E501
        :rtype: SolarSystemObject
        """
        return util.deserialize_model(dikt, cls)

    @property
    def kind(self):
        """Gets the kind of this SolarSystemObject.


        :return: The kind of this SolarSystemObject.
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this SolarSystemObject.


        :param kind: The kind of this SolarSystemObject.
        :type kind: str
        """
        if kind is None:
            raise ValueError("Invalid value for `kind`, must not be `None`")  # noqa: E501

        self._kind = kind

    @property
    def name(self):
        """Gets the name of this SolarSystemObject.


        :return: The name of this SolarSystemObject.
        :rtype: SolarSystemObjectName
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SolarSystemObject.


        :param name: The name of this SolarSystemObject.
        :type name: SolarSystemObjectName
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name
