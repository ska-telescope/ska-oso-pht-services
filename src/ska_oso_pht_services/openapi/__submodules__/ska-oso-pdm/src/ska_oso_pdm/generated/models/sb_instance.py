# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ska_oso_pdm.generated.models.base_model_ import Model
from ska_oso_pdm.generated.models.metadata import Metadata
from ska_oso_pdm.generated.models.python_arguments import PythonArguments
from ska_oso_pdm.generated.models.telescope import Telescope
from ska_oso_pdm.generated import util

from ska_oso_pdm.generated.models.metadata import Metadata  # noqa: E501
from ska_oso_pdm.generated.models.python_arguments import PythonArguments  # noqa: E501
from ska_oso_pdm.generated.models.telescope import Telescope  # noqa: E501

class SBInstance(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, interface=None, sbi_id=None, metadata=None, telescope=None, sbd_id=None, sbd_version=None, executed_on=None, subarray_id=None, runtime_args=None):  # noqa: E501
        """SBInstance - a model defined in OpenAPI

        :param interface: The interface of this SBInstance.  # noqa: E501
        :type interface: str
        :param sbi_id: The sbi_id of this SBInstance.  # noqa: E501
        :type sbi_id: str
        :param metadata: The metadata of this SBInstance.  # noqa: E501
        :type metadata: Metadata
        :param telescope: The telescope of this SBInstance.  # noqa: E501
        :type telescope: Telescope
        :param sbd_id: The sbd_id of this SBInstance.  # noqa: E501
        :type sbd_id: str
        :param sbd_version: The sbd_version of this SBInstance.  # noqa: E501
        :type sbd_version: int
        :param executed_on: The executed_on of this SBInstance.  # noqa: E501
        :type executed_on: datetime
        :param subarray_id: The subarray_id of this SBInstance.  # noqa: E501
        :type subarray_id: int
        :param runtime_args: The runtime_args of this SBInstance.  # noqa: E501
        :type runtime_args: PythonArguments
        """
        self.openapi_types = {
            'interface': str,
            'sbi_id': str,
            'metadata': Metadata,
            'telescope': Telescope,
            'sbd_id': str,
            'sbd_version': int,
            'executed_on': datetime,
            'subarray_id': int,
            'runtime_args': PythonArguments
        }

        self.attribute_map = {
            'interface': 'interface',
            'sbi_id': 'sbi_id',
            'metadata': 'metadata',
            'telescope': 'telescope',
            'sbd_id': 'sbd_id',
            'sbd_version': 'sbd_version',
            'executed_on': 'executed_on',
            'subarray_id': 'subarray_id',
            'runtime_args': 'runtime_args'
        }

        self._interface = interface
        self._sbi_id = sbi_id
        self._metadata = metadata
        self._telescope = telescope
        self._sbd_id = sbd_id
        self._sbd_version = sbd_version
        self._executed_on = executed_on
        self._subarray_id = subarray_id
        self._runtime_args = runtime_args

    @classmethod
    def from_dict(cls, dikt) -> 'SBInstance':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SBInstance of this SBInstance.  # noqa: E501
        :rtype: SBInstance
        """
        return util.deserialize_model(dikt, cls)

    @property
    def interface(self):
        """Gets the interface of this SBInstance.


        :return: The interface of this SBInstance.
        :rtype: str
        """
        return self._interface

    @interface.setter
    def interface(self, interface):
        """Sets the interface of this SBInstance.


        :param interface: The interface of this SBInstance.
        :type interface: str
        """
        if interface is None:
            raise ValueError("Invalid value for `interface`, must not be `None`")  # noqa: E501

        self._interface = interface

    @property
    def sbi_id(self):
        """Gets the sbi_id of this SBInstance.


        :return: The sbi_id of this SBInstance.
        :rtype: str
        """
        return self._sbi_id

    @sbi_id.setter
    def sbi_id(self, sbi_id):
        """Sets the sbi_id of this SBInstance.


        :param sbi_id: The sbi_id of this SBInstance.
        :type sbi_id: str
        """
        if sbi_id is None:
            raise ValueError("Invalid value for `sbi_id`, must not be `None`")  # noqa: E501

        self._sbi_id = sbi_id

    @property
    def metadata(self):
        """Gets the metadata of this SBInstance.


        :return: The metadata of this SBInstance.
        :rtype: Metadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this SBInstance.


        :param metadata: The metadata of this SBInstance.
        :type metadata: Metadata
        """
        if metadata is None:
            raise ValueError("Invalid value for `metadata`, must not be `None`")  # noqa: E501

        self._metadata = metadata

    @property
    def telescope(self):
        """Gets the telescope of this SBInstance.


        :return: The telescope of this SBInstance.
        :rtype: Telescope
        """
        return self._telescope

    @telescope.setter
    def telescope(self, telescope):
        """Sets the telescope of this SBInstance.


        :param telescope: The telescope of this SBInstance.
        :type telescope: Telescope
        """
        if telescope is None:
            raise ValueError("Invalid value for `telescope`, must not be `None`")  # noqa: E501

        self._telescope = telescope

    @property
    def sbd_id(self):
        """Gets the sbd_id of this SBInstance.


        :return: The sbd_id of this SBInstance.
        :rtype: str
        """
        return self._sbd_id

    @sbd_id.setter
    def sbd_id(self, sbd_id):
        """Sets the sbd_id of this SBInstance.


        :param sbd_id: The sbd_id of this SBInstance.
        :type sbd_id: str
        """

        self._sbd_id = sbd_id

    @property
    def sbd_version(self):
        """Gets the sbd_version of this SBInstance.


        :return: The sbd_version of this SBInstance.
        :rtype: int
        """
        return self._sbd_version

    @sbd_version.setter
    def sbd_version(self, sbd_version):
        """Sets the sbd_version of this SBInstance.


        :param sbd_version: The sbd_version of this SBInstance.
        :type sbd_version: int
        """

        self._sbd_version = sbd_version

    @property
    def executed_on(self):
        """Gets the executed_on of this SBInstance.


        :return: The executed_on of this SBInstance.
        :rtype: datetime
        """
        return self._executed_on

    @executed_on.setter
    def executed_on(self, executed_on):
        """Sets the executed_on of this SBInstance.


        :param executed_on: The executed_on of this SBInstance.
        :type executed_on: datetime
        """

        self._executed_on = executed_on

    @property
    def subarray_id(self):
        """Gets the subarray_id of this SBInstance.


        :return: The subarray_id of this SBInstance.
        :rtype: int
        """
        return self._subarray_id

    @subarray_id.setter
    def subarray_id(self, subarray_id):
        """Sets the subarray_id of this SBInstance.


        :param subarray_id: The subarray_id of this SBInstance.
        :type subarray_id: int
        """

        self._subarray_id = subarray_id

    @property
    def runtime_args(self):
        """Gets the runtime_args of this SBInstance.


        :return: The runtime_args of this SBInstance.
        :rtype: PythonArguments
        """
        return self._runtime_args

    @runtime_args.setter
    def runtime_args(self, runtime_args):
        """Sets the runtime_args of this SBInstance.


        :param runtime_args: The runtime_args of this SBInstance.
        :type runtime_args: PythonArguments
        """

        self._runtime_args = runtime_args
