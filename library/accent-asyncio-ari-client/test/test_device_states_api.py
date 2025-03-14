"""
    localhost:8088

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 5.1.1
    Generated by: https://openapi-generator.tech
"""


import unittest

import accent_appgateway_client


class TestDeviceStatesApi(unittest.TestCase):
    """DeviceStatesApi unit test stubs"""

    def setUp(self):
        self.api = accent_appgateway_client.api.device_states_api.DeviceStatesApi()

    def tearDown(self):
        pass

    def test_device_states_device_name_delete(self):
        """Test case for device_states_device_name_delete

        Destroy a device-state controlled by ARI.  # noqa: E501
        """
        pass

    def test_device_states_device_name_get(self):
        """Test case for device_states_device_name_get

        Retrieve the current state of a device.  # noqa: E501
        """
        pass

    def test_device_states_device_name_put(self):
        """Test case for device_states_device_name_put

        Change the state of a device controlled by ARI. (Note - implicitly creates the device state).  # noqa: E501
        """
        pass

    def test_device_states_get(self):
        """Test case for device_states_get

        List all ARI controlled device states.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
