# Copyright 2023 Accent Communications

from __future__ import annotations

import unittest
from typing import Any

from hamcrest import assert_that, equal_to, has_key, is_not

from accent_provd.phonebook import (
    add_accent_phonebook_url,
    add_accent_phonebook_url_from_format,
)


class TestAddAccentPhonebookURL(unittest.TestCase):
    def setUp(self) -> None:
        self.raw_config: dict[str, Any] = {
            'X_accent_phonebook_ip': '8.8.8.8',
            'X_accent_user_uuid': '12-345',
        }

    def test_add_accent_phonebook_url_minimal(self) -> None:
        add_accent_phonebook_url(self.raw_config, 'acme')

        expected = 'http://8.8.8.8:9498/0.1/directories/input/default/acme?accent_user_uuid=12-345'
        assert_that(self.raw_config['XX_accent_phonebook_url'], equal_to(expected))

    def test_add_accent_phonebook_url_full(self) -> None:
        add_accent_phonebook_url(
            self.raw_config, 'acme', entry_point='ep', qs_prefix='p=1', qs_suffix='s=2'
        )

        expected = (
            'http://8.8.8.8:9498'
            '/0.1/directories/ep/default/acme?p=1&accent_user_uuid=12-345&s=2'
        )
        assert_that(self.raw_config['XX_accent_phonebook_url'], equal_to(expected))


class TestAddAccentPhonebookURLFromFormat(unittest.TestCase):
    def setUp(self) -> None:
        self.url_format = (
            '{scheme}://{hostname}:{port}/{profile}?accent_user_uuid={user_uuid}'
        )
        self.raw_config: dict[str, Any] = {
            'X_accent_phonebook_ip': '8.8.8.8',
            'X_accent_user_uuid': '12-345',
        }

    def test_add_accent_phonebook_url_from_format_no_ip(self) -> None:
        del self.raw_config['X_accent_phonebook_ip']

        add_accent_phonebook_url_from_format(self.raw_config, self.url_format)

        assert_that(self.raw_config, is_not(has_key('XX_accent_phonebook_url')))

    def test_add_accent_phonebook_url_from_format_no_user_uuid(self) -> None:
        del self.raw_config['X_accent_user_uuid']

        add_accent_phonebook_url_from_format(self.raw_config, self.url_format)

        assert_that(self.raw_config, is_not(has_key('XX_accent_phonebook_url')))

    def test_add_accent_phonebook_url_from_format_full(self) -> None:
        self.raw_config['X_accent_phonebook_scheme'] = 'https'
        self.raw_config['X_accent_phonebook_port'] = 4242

        add_accent_phonebook_url_from_format(self.raw_config, self.url_format)

        expected = 'https://8.8.8.8:4242/default?accent_user_uuid=12-345'
        assert_that(self.raw_config['XX_accent_phonebook_url'], equal_to(expected))
