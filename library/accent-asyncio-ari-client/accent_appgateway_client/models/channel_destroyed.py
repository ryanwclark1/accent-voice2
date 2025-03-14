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


class ChannelDestroyed(object):
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
        'cause': 'int',
        'cause_txt': 'str',
        'channel': 'Channel'
    }

    attribute_map = {
        'cause': 'cause',
        'cause_txt': 'cause_txt',
        'channel': 'channel'
    }

    def __init__(self, cause=None, cause_txt=None, channel=None, local_vars_configuration=None):  # noqa: E501
        """ChannelDestroyed - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._cause = None
        self._cause_txt = None
        self._channel = None
        self.discriminator = None

        self.cause = cause
        self.cause_txt = cause_txt
        self.channel = channel

    @property
    def cause(self):
        """Gets the cause of this ChannelDestroyed.  # noqa: E501

        Integer representation of the cause of the hangup  # noqa: E501

        :return: The cause of this ChannelDestroyed.  # noqa: E501
        :rtype: int
        """
        return self._cause

    @cause.setter
    def cause(self, cause):
        """Sets the cause of this ChannelDestroyed.

        Integer representation of the cause of the hangup  # noqa: E501

        :param cause: The cause of this ChannelDestroyed.  # noqa: E501
        :type cause: int
        """
        if self.local_vars_configuration.client_side_validation and cause is None:  # noqa: E501
            raise ValueError("Invalid value for `cause`, must not be `None`")  # noqa: E501

        self._cause = cause

    @property
    def cause_txt(self):
        """Gets the cause_txt of this ChannelDestroyed.  # noqa: E501

        Text representation of the cause of the hangup  # noqa: E501

        :return: The cause_txt of this ChannelDestroyed.  # noqa: E501
        :rtype: str
        """
        return self._cause_txt

    @cause_txt.setter
    def cause_txt(self, cause_txt):
        """Sets the cause_txt of this ChannelDestroyed.

        Text representation of the cause of the hangup  # noqa: E501

        :param cause_txt: The cause_txt of this ChannelDestroyed.  # noqa: E501
        :type cause_txt: str
        """
        if self.local_vars_configuration.client_side_validation and cause_txt is None:  # noqa: E501
            raise ValueError("Invalid value for `cause_txt`, must not be `None`")  # noqa: E501

        self._cause_txt = cause_txt

    @property
    def channel(self):
        """Gets the channel of this ChannelDestroyed.  # noqa: E501


        :return: The channel of this ChannelDestroyed.  # noqa: E501
        :rtype: Channel
        """
        return self._channel

    @channel.setter
    def channel(self, channel):
        """Sets the channel of this ChannelDestroyed.


        :param channel: The channel of this ChannelDestroyed.  # noqa: E501
        :type channel: Channel
        """
        if self.local_vars_configuration.client_side_validation and channel is None:  # noqa: E501
            raise ValueError("Invalid value for `channel`, must not be `None`")  # noqa: E501

        self._channel = channel

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
        if not isinstance(other, ChannelDestroyed):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChannelDestroyed):
            return True

        return self.to_dict() != other.to_dict()
