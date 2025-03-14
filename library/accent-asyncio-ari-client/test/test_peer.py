"""
    localhost:8088

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 5.1.1
    Generated by: https://openapi-generator.tech
"""


import unittest

from accent_appgateway_client.models.peer import Peer


class TestPeer(unittest.TestCase):
    """Peer unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Peer
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = accent_appgateway_client.models.peer.Peer()
        if include_optional:
            return Peer(address='0', cause='0', peer_status='0', port='0', time='0')
        else:
            return Peer(
                peer_status='0',
            )

    def testPeer(self):
        """Test Peer"""
        self.make_instance(include_optional=False)
        self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
