"""
    localhost:8088

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 5.1.1
    Generated by: https://openapi-generator.tech
"""


import unittest

from accent_appgateway_client.models.application import Application


class TestApplication(unittest.TestCase):
    """Application unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Application
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = accent_appgateway_client.models.application.Application()
        if include_optional:
            return Application(
                bridge_ids=['0'],
                channel_ids=['0'],
                device_names=['0'],
                endpoint_ids=['0'],
                events_allowed=[None],
                events_disallowed=[None],
                name='0',
            )
        else:
            return Application(
                bridge_ids=['0'],
                channel_ids=['0'],
                device_names=['0'],
                endpoint_ids=['0'],
                events_allowed=[None],
                events_disallowed=[None],
                name='0',
            )

    def testApplication(self):
        """Test Application"""
        self.make_instance(include_optional=False)
        self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
