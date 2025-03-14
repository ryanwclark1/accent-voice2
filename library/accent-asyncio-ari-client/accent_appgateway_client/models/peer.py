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


class Peer(object):
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
        'address': 'str',
        'cause': 'str',
        'peer_status': 'str',
        'port': 'str',
        'time': 'str'
    }

    attribute_map = {
        'address': 'address',
        'cause': 'cause',
        'peer_status': 'peer_status',
        'port': 'port',
        'time': 'time'
    }

    def __init__(self, address=None, cause=None, peer_status=None, port=None, time=None, local_vars_configuration=None):  # noqa: E501
        """Peer - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._address = None
        self._cause = None
        self._peer_status = None
        self._port = None
        self._time = None
        self.discriminator = None

        if address is not None:
            self.address = address
        if cause is not None:
            self.cause = cause
        self.peer_status = peer_status
        if port is not None:
            self.port = port
        if time is not None:
            self.time = time

    @property
    def address(self):
        """Gets the address of this Peer.  # noqa: E501

        The IP address of the peer.  # noqa: E501

        :return: The address of this Peer.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this Peer.

        The IP address of the peer.  # noqa: E501

        :param address: The address of this Peer.  # noqa: E501
        :type address: str
        """

        self._address = address

    @property
    def cause(self):
        """Gets the cause of this Peer.  # noqa: E501

        An optional reason associated with the change in peer_status.  # noqa: E501

        :return: The cause of this Peer.  # noqa: E501
        :rtype: str
        """
        return self._cause

    @cause.setter
    def cause(self, cause):
        """Sets the cause of this Peer.

        An optional reason associated with the change in peer_status.  # noqa: E501

        :param cause: The cause of this Peer.  # noqa: E501
        :type cause: str
        """

        self._cause = cause

    @property
    def peer_status(self):
        """Gets the peer_status of this Peer.  # noqa: E501

        The current state of the peer. Note that the values of the status are dependent on the underlying peer technology.  # noqa: E501

        :return: The peer_status of this Peer.  # noqa: E501
        :rtype: str
        """
        return self._peer_status

    @peer_status.setter
    def peer_status(self, peer_status):
        """Sets the peer_status of this Peer.

        The current state of the peer. Note that the values of the status are dependent on the underlying peer technology.  # noqa: E501

        :param peer_status: The peer_status of this Peer.  # noqa: E501
        :type peer_status: str
        """
        if self.local_vars_configuration.client_side_validation and peer_status is None:  # noqa: E501
            raise ValueError("Invalid value for `peer_status`, must not be `None`")  # noqa: E501

        self._peer_status = peer_status

    @property
    def port(self):
        """Gets the port of this Peer.  # noqa: E501

        The port of the peer.  # noqa: E501

        :return: The port of this Peer.  # noqa: E501
        :rtype: str
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this Peer.

        The port of the peer.  # noqa: E501

        :param port: The port of this Peer.  # noqa: E501
        :type port: str
        """

        self._port = port

    @property
    def time(self):
        """Gets the time of this Peer.  # noqa: E501

        The last known time the peer was contacted.  # noqa: E501

        :return: The time of this Peer.  # noqa: E501
        :rtype: str
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this Peer.

        The last known time the peer was contacted.  # noqa: E501

        :param time: The time of this Peer.  # noqa: E501
        :type time: str
        """

        self._time = time

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
        if not isinstance(other, Peer):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Peer):
            return True

        return self.to_dict() != other.to_dict()
