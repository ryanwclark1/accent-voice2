# Copyright 2023 Accent Communications

import unittest
from io import StringIO
from unittest.mock import Mock

from accent_dao.alchemy.conference import Conference

from accent_confgend.generators.tests.util import assert_config_equal

from ..confbridge_conf import _ConfBridgeConf


class TestConfBridgeConf(unittest.TestCase):
    def setUp(self):
        self.conference_dao = Mock()
        self.conference_dao.find_all_by.return_value = []
        self.confbridge_conf = _ConfBridgeConf(self.conference_dao)
        self.output = StringIO()

    def test_gen_bridge_profile(self):
        conferences = [
            Conference(id=1, max_users=50, record=True),
            Conference(id=2, max_users=0, record=False),
        ]
        self.confbridge_conf._gen_bridge_profile(conferences, self.output)

        assert_config_equal(
            self.output.getvalue(),
            '''
            [accent-bridge-profile-1](accent_default_bridge)
            type = bridge
            max_members = 50
            record_conference = yes

            [accent-bridge-profile-2](accent_default_bridge)
            type = bridge
            max_members = 0
            record_conference = no
        ''',
        )

    def test_gen_user_profile(self):
        conferences = [
            Conference(
                id=1,
                admin_pin=None,
                music_on_hold=None,
                quiet_join_leave=False,
                announce_join_leave=False,
                announce_user_count=False,
                announce_only_user=False,
            ),
            Conference(
                id=2,
                admin_pin='1234',
                music_on_hold='Music',
                quiet_join_leave=True,
                announce_join_leave=True,
                announce_user_count=True,
                announce_only_user=True,
            ),
        ]
        self.confbridge_conf._gen_user_profile(conferences, self.output)

        assert_config_equal(
            self.output.getvalue(),
            '''
            [accent-user-profile-1](accent_default_user)
            type = user
            quiet = no
            announce_join_leave = no
            announce_user_count = no
            announce_only_user = no

            [accent-user-profile-2](accent_default_user)
            type = user
            quiet = yes
            announce_join_leave = yes
            announce_user_count = yes
            announce_only_user = yes
            music_on_hold_when_empty = yes
            music_on_hold_class = Music

            [accent-admin-profile-2](accent-user-profile-2)
            admin = yes
        ''',
        )

    def test_gen_default_menu(self):
        self.confbridge_conf._gen_default_menu(self.output)

        assert_config_equal(
            self.output.getvalue(),
            '''
        [accent-default-user-menu]
        type = menu
        * = playback_and_continue(dir-multi1&digits/1&confbridge-mute-out&digits/4&confbridge-dec-list-vol-out&digits/5&confbridge-rest-list-vol-out&digits/6&confbridge-inc-list-vol-out&digits/7&confbridge-dec-talk-vol-out&digits/8&confbridge-rest-talk-vol-out&digits/9&confbridge-inc-talk-vol-out)
        1 = toggle_mute
        4 = decrease_listening_volume
        5 = reset_listening_volume
        6 = increase_listening_volume
        7 = decrease_talking_volume
        8 = reset_talking_volume
        9 = increase_talking_volume

        [accent-default-admin-menu](accent-default-user-menu)
        * = playback_and_continue(dir-multi1&digits/1&confbridge-mute-out&digits/2&confbridge-lock-out&digits/3&confbridge-remove-last-out&digits/4&confbridge-dec-list-vol-out&digits/5&confbridge-rest-list-vol-out&digits/6&confbridge-inc-list-vol-out&digits/7&confbridge-dec-talk-vol-out&digits/8&confbridge-rest-talk-vol-out&digits/9&confbridge-inc-talk-vol-out)
        2 = admin_toggle_conference_lock
        3 = admin_kick_last
        0 = admin_toggle_mute_participants
        ''',
        )
