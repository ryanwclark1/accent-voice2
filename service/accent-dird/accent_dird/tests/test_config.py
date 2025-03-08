# Copyright 2023 Accent Communications

import logging
from unittest import TestCase
from unittest.mock import Mock, patch

from hamcrest import assert_that, equal_to, has_entries

from accent_dird import config


@patch('builtins.print', Mock())
@patch('accent_dird.config.open', create=True)
class TestConfig(TestCase):
    def test_load_when_no_args_and_no_default_config_file_then_default_values(self, mock_open):
        mock_open.side_effect = OSError('no such file')
        config._DEFAULT_CONFIG = {
            'config': 'default',
            'config_file': '/etc/accent-dird/config.yml',
            'extra_config_files': '/etc/accent-dird/conf.d/',
        }

        result = config.load([])

        assert_that(result, has_entries(config._DEFAULT_CONFIG))

    def test_load_when_config_file_in_argv_then_read_config_from_file(self, _):
        result = config.load(['-c', 'my_file'])

        assert_that(result['config_file'], equal_to('my_file'))

    def test_load_when_user_in_argv_then_ignore_default_value(self, mock_open):
        mock_open.side_effect = OSError('no such file')

        result = config.load(['-u', 'my_user'])

        assert_that(result['user'], equal_to('my_user'))

    def test_load_when_debug_in_argv_then_ignore_default_value(self, mock_open):
        mock_open.side_effect = OSError('no such file')

        result = config.load(['-d'])

        assert_that(result['debug'], equal_to(True))

    def test_load_when_log_level_in_argv_then_ignore_default_value(self, mock_open):
        mock_open.side_effect = OSError('no such file')

        result = config.load(['-l', 'ERROR'])

        assert_that(result['log_level'], equal_to(logging.ERROR))
