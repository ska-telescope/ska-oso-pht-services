# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ska_oso_pdm.generated.models.base_model_ import Model
from ska_oso_pdm.generated import util


class Metadata(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, version=None, created_by=None, created_on=None, last_modified_by=None, last_modified_on=None):  # noqa: E501
        """Metadata - a model defined in OpenAPI

        :param version: The version of this Metadata.  # noqa: E501
        :type version: int
        :param created_by: The created_by of this Metadata.  # noqa: E501
        :type created_by: str
        :param created_on: The created_on of this Metadata.  # noqa: E501
        :type created_on: datetime
        :param last_modified_by: The last_modified_by of this Metadata.  # noqa: E501
        :type last_modified_by: str
        :param last_modified_on: The last_modified_on of this Metadata.  # noqa: E501
        :type last_modified_on: datetime
        """
        self.openapi_types = {
            'version': int,
            'created_by': str,
            'created_on': datetime,
            'last_modified_by': str,
            'last_modified_on': datetime
        }

        self.attribute_map = {
            'version': 'version',
            'created_by': 'created_by',
            'created_on': 'created_on',
            'last_modified_by': 'last_modified_by',
            'last_modified_on': 'last_modified_on'
        }

        self._version = version
        self._created_by = created_by
        self._created_on = created_on
        self._last_modified_by = last_modified_by
        self._last_modified_on = last_modified_on

    @classmethod
    def from_dict(cls, dikt) -> 'Metadata':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Metadata of this Metadata.  # noqa: E501
        :rtype: Metadata
        """
        return util.deserialize_model(dikt, cls)

    @property
    def version(self):
        """Gets the version of this Metadata.


        :return: The version of this Metadata.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Metadata.


        :param version: The version of this Metadata.
        :type version: int
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def created_by(self):
        """Gets the created_by of this Metadata.


        :return: The created_by of this Metadata.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this Metadata.


        :param created_by: The created_by of this Metadata.
        :type created_by: str
        """
        if created_by is None:
            raise ValueError("Invalid value for `created_by`, must not be `None`")  # noqa: E501

        self._created_by = created_by

    @property
    def created_on(self):
        """Gets the created_on of this Metadata.


        :return: The created_on of this Metadata.
        :rtype: datetime
        """
        return self._created_on

    @created_on.setter
    def created_on(self, created_on):
        """Sets the created_on of this Metadata.


        :param created_on: The created_on of this Metadata.
        :type created_on: datetime
        """
        if created_on is None:
            raise ValueError("Invalid value for `created_on`, must not be `None`")  # noqa: E501

        self._created_on = created_on

    @property
    def last_modified_by(self):
        """Gets the last_modified_by of this Metadata.


        :return: The last_modified_by of this Metadata.
        :rtype: str
        """
        return self._last_modified_by

    @last_modified_by.setter
    def last_modified_by(self, last_modified_by):
        """Sets the last_modified_by of this Metadata.


        :param last_modified_by: The last_modified_by of this Metadata.
        :type last_modified_by: str
        """

        self._last_modified_by = last_modified_by

    @property
    def last_modified_on(self):
        """Gets the last_modified_on of this Metadata.


        :return: The last_modified_on of this Metadata.
        :rtype: datetime
        """
        return self._last_modified_on

    @last_modified_on.setter
    def last_modified_on(self, last_modified_on):
        """Sets the last_modified_on of this Metadata.


        :param last_modified_on: The last_modified_on of this Metadata.
        :type last_modified_on: datetime
        """

        self._last_modified_on = last_modified_on
