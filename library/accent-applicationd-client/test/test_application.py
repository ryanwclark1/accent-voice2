# coding: utf-8

"""
    Accent applicationd

    Applicationd  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import accent_applicationd_client
from accent_applicationd_client.models.application import Application  # noqa: E501
from accent_applicationd_client.rest import ApiException

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
            optional params are included """
        # model = accent_applicationd_client.models.application.Application()  # noqa: E501
        if include_optional :
            return Application(
                uuid = '0'
            )
        else :
            return Application(
                uuid = '0',
        )

    def testApplication(self):
        """Test Application"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
