"""
    localhost:8088

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 5.1.1
    Generated by: https://openapi-generator.tech
"""


import unittest

import accent_appgateway_client


class TestBridgesApi(unittest.TestCase):
    """BridgesApi unit test stubs"""

    def setUp(self):
        self.api = accent_appgateway_client.api.bridges_api.BridgesApi()

    def tearDown(self):
        pass

    def test_bridges_bridge_id_add_channel_post(self):
        """Test case for bridges_bridge_id_add_channel_post

        Add a channel to a bridge.  # noqa: E501
        """
        pass

    def test_bridges_bridge_id_delete(self):
        """Test case for bridges_bridge_id_delete

        Shut down a bridge.  # noqa: E501
        """
        pass

    def test_bridges_bridge_id_get(self):
        """Test case for bridges_bridge_id_get

        Get bridge details.  # noqa: E501
        """
        pass

    def test_bridges_bridge_id_moh_delete(self):
        """Test case for bridges_bridge_id_moh_delete

        Stop playing music on hold to a bridge.  # noqa: E501
        """
        pass

    def test_bridges_bridge_id_moh_post(self):
        """Test case for bridges_bridge_id_moh_post

        Play music on hold to a bridge or change the MOH class that is playing.  # noqa: E501
        """
        pass

    def test_bridges_bridge_id_play_playback_id_post(self):
        """Test case for bridges_bridge_id_play_playback_id_post

        Start playback of media on a bridge.  # noqa: E501
        """
        pass

    def test_bridges_bridge_id_play_post(self):
        """Test case for bridges_bridge_id_play_post

        Start playback of media on a bridge.  # noqa: E501
        """
        pass

    def test_bridges_bridge_id_post(self):
        """Test case for bridges_bridge_id_post

        Create a new bridge or updates an existing one.  # noqa: E501
        """
        pass

    def test_bridges_bridge_id_record_post(self):
        """Test case for bridges_bridge_id_record_post

        Start a recording.  # noqa: E501
        """
        pass

    def test_bridges_bridge_id_remove_channel_post(self):
        """Test case for bridges_bridge_id_remove_channel_post

        Remove a channel from a bridge.  # noqa: E501
        """
        pass

    def test_bridges_bridge_id_video_source_channel_id_post(self):
        """Test case for bridges_bridge_id_video_source_channel_id_post

        Set a channel as the video source in a multi-party mixing bridge. This operation has no effect on bridges with two or fewer participants.  # noqa: E501
        """
        pass

    def test_bridges_bridge_id_video_source_delete(self):
        """Test case for bridges_bridge_id_video_source_delete

        Removes any explicit video source in a multi-party mixing bridge. This operation has no effect on bridges with two or fewer participants. When no explicit video source is set, talk detection will be used to determine the active video stream.  # noqa: E501
        """
        pass

    def test_bridges_get(self):
        """Test case for bridges_get

        List all active bridges in Asterisk.  # noqa: E501
        """
        pass

    def test_bridges_post(self):
        """Test case for bridges_post

        Create a new bridge.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
