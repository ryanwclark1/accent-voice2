# Copyright 2023 Accent Communications

from __future__ import annotations

import unittest

from hamcrest import assert_that, equal_to, has_key, not_

from accent_provd.phoned_users import add_accent_phoned_user_service_url


class TestAddAccentPhonedUserServiceURL(unittest.TestCase):
    def setUp(self) -> None:
        self.raw_config = {
            'X_accent_phonebook_ip': '8.8.8.8',
            'X_accent_user_uuid': '12-345',
        }

    def test_add_accent_phoned_user_service_url(self) -> None:
        add_accent_phoned_user_service_url(self.raw_config, 'acme', 'dnd')

        expected = 'http://8.8.8.8:9498/0.1/acme/users/12-345/services/dnd/enable'
        assert_that(
            self.raw_config['XX_accent_phoned_user_service_dnd_enabled_url'],
            equal_to(expected),
        )

        expected = 'http://8.8.8.8:9498/0.1/acme/users/12-345/services/dnd/disable'
        assert_that(
            self.raw_config['XX_accent_phoned_user_service_dnd_disabled_url'],
            equal_to(expected),
        )

    def test_no_user_uuid_no_url(self) -> None:
        del self.raw_config['X_accent_user_uuid']
        add_accent_phoned_user_service_url(self.raw_config, 'acme', 'dnd')
        assert_that(
            self.raw_config,
            not_(has_key('XX_accent_phoned_user_service_dnd_enabled_url')),
        )
        assert_that(
            self.raw_config,
            not_(has_key('XX_accent_phoned_user_service_dnd_disabled_url')),
        )

    def test_no_hostname_no_url(self) -> None:
        del self.raw_config['X_accent_phonebook_ip']
        add_accent_phoned_user_service_url(self.raw_config, 'acme', 'dnd')
        assert_that(
            self.raw_config,
            not_(has_key('XX_accent_phoned_user_service_dnd_enabled_url')),
        )
        assert_that(
            self.raw_config,
            not_(has_key('XX_accent_phoned_user_service_dnd_disabled_url')),
        )
