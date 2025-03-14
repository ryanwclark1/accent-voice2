# coding: utf-8

"""
    localhost:8088

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 5.1.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from accent_appgateway_client.configuration import Configuration


class BridgeBlindTransferAllOf(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'bridge': 'Bridge',
        'channel': 'Channel',
        'context': 'str',
        'exten': 'str',
        'is_external': 'bool',
        'replace_channel': 'Channel',
        'result': 'str',
        'transferee': 'Channel'
    }

    attribute_map = {
        'bridge': 'bridge',
        'channel': 'channel',
        'context': 'context',
        'exten': 'exten',
        'is_external': 'is_external',
        'replace_channel': 'replace_channel',
        'result': 'result',
        'transferee': 'transferee'
    }

    def __init__(self, bridge=None, channel=None, context=None, exten=None, is_external=None, replace_channel=None, result=None, transferee=None, local_vars_configuration=None):  # noqa: E501
        """BridgeBlindTransferAllOf - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._bridge = None
        self._channel = None
        self._context = None
        self._exten = None
        self._is_external = None
        self._replace_channel = None
        self._result = None
        self._transferee = None
        self.discriminator = None

        if bridge is not None:
            self.bridge = bridge
        self.channel = channel
        self.context = context
        self.exten = exten
        self.is_external = is_external
        if replace_channel is not None:
            self.replace_channel = replace_channel
        self.result = result
        if transferee is not None:
            self.transferee = transferee

    @property
    def bridge(self):
        """Gets the bridge of this BridgeBlindTransferAllOf.  # noqa: E501


        :return: The bridge of this BridgeBlindTransferAllOf.  # noqa: E501
        :rtype: Bridge
        """
        return self._bridge

    @bridge.setter
    def bridge(self, bridge):
        """Sets the bridge of this BridgeBlindTransferAllOf.


        :param bridge: The bridge of this BridgeBlindTransferAllOf.  # noqa: E501
        :type bridge: Bridge
        """

        self._bridge = bridge

    @property
    def channel(self):
        """Gets the channel of this BridgeBlindTransferAllOf.  # noqa: E501


        :return: The channel of this BridgeBlindTransferAllOf.  # noqa: E501
        :rtype: Channel
        """
        return self._channel

    @channel.setter
    def channel(self, channel):
        """Sets the channel of this BridgeBlindTransferAllOf.


        :param channel: The channel of this BridgeBlindTransferAllOf.  # noqa: E501
        :type channel: Channel
        """
        if self.local_vars_configuration.client_side_validation and channel is None:  # noqa: E501
            raise ValueError("Invalid value for `channel`, must not be `None`")  # noqa: E501

        self._channel = channel

    @property
    def context(self):
        """Gets the context of this BridgeBlindTransferAllOf.  # noqa: E501

        The context transferred to  # noqa: E501

        :return: The context of this BridgeBlindTransferAllOf.  # noqa: E501
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context):
        """Sets the context of this BridgeBlindTransferAllOf.

        The context transferred to  # noqa: E501

        :param context: The context of this BridgeBlindTransferAllOf.  # noqa: E501
        :type context: str
        """
        if self.local_vars_configuration.client_side_validation and context is None:  # noqa: E501
            raise ValueError("Invalid value for `context`, must not be `None`")  # noqa: E501

        self._context = context

    @property
    def exten(self):
        """Gets the exten of this BridgeBlindTransferAllOf.  # noqa: E501

        The extension transferred to  # noqa: E501

        :return: The exten of this BridgeBlindTransferAllOf.  # noqa: E501
        :rtype: str
        """
        return self._exten

    @exten.setter
    def exten(self, exten):
        """Sets the exten of this BridgeBlindTransferAllOf.

        The extension transferred to  # noqa: E501

        :param exten: The exten of this BridgeBlindTransferAllOf.  # noqa: E501
        :type exten: str
        """
        if self.local_vars_configuration.client_side_validation and exten is None:  # noqa: E501
            raise ValueError("Invalid value for `exten`, must not be `None`")  # noqa: E501

        self._exten = exten

    @property
    def is_external(self):
        """Gets the is_external of this BridgeBlindTransferAllOf.  # noqa: E501

        Whether the transfer was externally initiated or not  # noqa: E501

        :return: The is_external of this BridgeBlindTransferAllOf.  # noqa: E501
        :rtype: bool
        """
        return self._is_external

    @is_external.setter
    def is_external(self, is_external):
        """Sets the is_external of this BridgeBlindTransferAllOf.

        Whether the transfer was externally initiated or not  # noqa: E501

        :param is_external: The is_external of this BridgeBlindTransferAllOf.  # noqa: E501
        :type is_external: bool
        """
        if self.local_vars_configuration.client_side_validation and is_external is None:  # noqa: E501
            raise ValueError("Invalid value for `is_external`, must not be `None`")  # noqa: E501

        self._is_external = is_external

    @property
    def replace_channel(self):
        """Gets the replace_channel of this BridgeBlindTransferAllOf.  # noqa: E501


        :return: The replace_channel of this BridgeBlindTransferAllOf.  # noqa: E501
        :rtype: Channel
        """
        return self._replace_channel

    @replace_channel.setter
    def replace_channel(self, replace_channel):
        """Sets the replace_channel of this BridgeBlindTransferAllOf.


        :param replace_channel: The replace_channel of this BridgeBlindTransferAllOf.  # noqa: E501
        :type replace_channel: Channel
        """

        self._replace_channel = replace_channel

    @property
    def result(self):
        """Gets the result of this BridgeBlindTransferAllOf.  # noqa: E501

        The result of the transfer attempt  # noqa: E501

        :return: The result of this BridgeBlindTransferAllOf.  # noqa: E501
        :rtype: str
        """
        return self._result

    @result.setter
    def result(self, result):
        """Sets the result of this BridgeBlindTransferAllOf.

        The result of the transfer attempt  # noqa: E501

        :param result: The result of this BridgeBlindTransferAllOf.  # noqa: E501
        :type result: str
        """
        if self.local_vars_configuration.client_side_validation and result is None:  # noqa: E501
            raise ValueError("Invalid value for `result`, must not be `None`")  # noqa: E501

        self._result = result

    @property
    def transferee(self):
        """Gets the transferee of this BridgeBlindTransferAllOf.  # noqa: E501


        :return: The transferee of this BridgeBlindTransferAllOf.  # noqa: E501
        :rtype: Channel
        """
        return self._transferee

    @transferee.setter
    def transferee(self, transferee):
        """Sets the transferee of this BridgeBlindTransferAllOf.


        :param transferee: The transferee of this BridgeBlindTransferAllOf.  # noqa: E501
        :type transferee: Channel
        """

        self._transferee = transferee

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, BridgeBlindTransferAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BridgeBlindTransferAllOf):
            return True

        return self.to_dict() != other.to_dict()
