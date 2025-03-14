# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import ANY, patch
from unittest.mock import sentinel as s

from hamcrest import assert_that, equal_to

from accent_phoned.bin import daemon


@patch('accent_phoned.bin.daemon.change_user')
@patch('accent_phoned.bin.daemon.setup_logging')
@patch('accent_phoned.bin.daemon.Controller')
@patch('accent_phoned.bin.daemon.load_config')
class TestAccentDird(TestCase):
    def test_main_injects_argv_into_config_loading(
        self, load_config, controller_init, setup_logging, change_user
    ):
        daemon.main(s.argv)

        load_config.assert_called_once_with(ANY, s.argv)

    def test_main_injects_config_in_controller(
        self, load_config, controller_init, setup_logging, change_user
    ):
        config = load_config.return_value

        daemon.main(s.argv)

        controller_init.assert_called_once_with(config)

    def test_main_setup_logging(
        self, load_config, controller_init, setup_logging, change_user
    ):
        load_config.return_value = {
            'debug': s.debug,
            'log_filename': s.log_filename,
            'log_level': s.log_level,
            'user': s.user,
        }

        daemon.main(s.argv)

        setup_logging.assert_called_once_with(
            s.log_filename, debug=s.debug, log_level=s.log_level
        )

    def test_main_when_config_user_then_change_user(
        self, load_config, controller_init, setup_logging, change_user
    ):
        load_config.return_value = {
            'debug': s.debug,
            'log_filename': s.log_filename,
            'log_level': s.log_level,
            'user': s.user,
        }

        daemon.main(s.argv)

        change_user.assert_called_once_with(s.user)

    def test_main_when_no_config_user_then_dont_change_user(
        self, load_config, controller_init, setup_logging, change_user
    ):
        load_config.return_value = {
            'debug': s.debug,
            'log_filename': s.log_filename,
            'log_level': s.log_level,
            'user': None,
        }

        daemon.main(s.argv)

        assert_that(change_user.call_count, equal_to(0))

    def test_main_calls_controller_run(
        self, load_config, controller_init, setup_logging, change_user
    ):
        controller = controller_init.return_value
        load_config.return_value = {
            'debug': s.debug,
            'log_filename': s.log_filename,
            'log_level': s.log_level,
            'user': None,
        }

        daemon.main(s.argv)

        controller.run.assert_called_once_with()
