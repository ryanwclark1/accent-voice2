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


class ChannelVarsetAllOf(object):
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
        'channel': 'Channel',
        'value': 'str',
        'variable': 'str'
    }

    attribute_map = {
        'channel': 'channel',
        'value': 'value',
        'variable': 'variable'
    }

    def __init__(self, channel=None, value=None, variable=None, local_vars_configuration=None):  # noqa: E501
        """ChannelVarsetAllOf - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._channel = None
        self._value = None
        self._variable = None
        self.discriminator = None

        if channel is not None:
            self.channel = channel
        self.value = value
        self.variable = variable

    @property
    def channel(self):
        """Gets the channel of this ChannelVarsetAllOf.  # noqa: E501


        :return: The channel of this ChannelVarsetAllOf.  # noqa: E501
        :rtype: Channel
        """
        return self._channel

    @channel.setter
    def channel(self, channel):
        """Sets the channel of this ChannelVarsetAllOf.


        :param channel: The channel of this ChannelVarsetAllOf.  # noqa: E501
        :type channel: Channel
        """

        self._channel = channel

    @property
    def value(self):
        """Gets the value of this ChannelVarsetAllOf.  # noqa: E501

        The new value of the variable.  # noqa: E501

        :return: The value of this ChannelVarsetAllOf.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this ChannelVarsetAllOf.

        The new value of the variable.  # noqa: E501

        :param value: The value of this ChannelVarsetAllOf.  # noqa: E501
        :type value: str
        """
        if self.local_vars_configuration.client_side_validation and value is None:  # noqa: E501
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501

        self._value = value

    @property
    def variable(self):
        """Gets the variable of this ChannelVarsetAllOf.  # noqa: E501

        The variable that changed.  # noqa: E501

        :return: The variable of this ChannelVarsetAllOf.  # noqa: E501
        :rtype: str
        """
        return self._variable

    @variable.setter
    def variable(self, variable):
        """Sets the variable of this ChannelVarsetAllOf.

        The variable that changed.  # noqa: E501

        :param variable: The variable of this ChannelVarsetAllOf.  # noqa: E501
        :type variable: str
        """
        if self.local_vars_configuration.client_side_validation and variable is None:  # noqa: E501
            raise ValueError("Invalid value for `variable`, must not be `None`")  # noqa: E501

        self._variable = variable

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
        if not isinstance(other, ChannelVarsetAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChannelVarsetAllOf):
            return True

        return self.to_dict() != other.to_dict()
