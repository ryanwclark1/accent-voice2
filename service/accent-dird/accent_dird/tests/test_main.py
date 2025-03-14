# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import patch
from unittest.mock import sentinel as s

from hamcrest import assert_that, equal_to

from ..main import main


@patch('accent_dird.main.set_accent_uuid')
@patch('accent_dird.main.change_user')
@patch('accent_dird.main.accent_logging')
@patch('accent_dird.main.Controller')
@patch('accent_dird.main.load_config')
class TestAccentDird(TestCase):
    def test_main_injects_argv_into_config_loading(self, load_config, *_):
        main(s.argv)

        load_config.assert_called_once_with(s.argv)

    def test_main_injects_config_in_controller(self, load_config, controller_init, *_):
        config = load_config.return_value

        main(s.argv)

        controller_init.assert_called_once_with(config)

    def test_main_setup_logging(self, load_config, _, accent_logging, *__):
        load_config.return_value = {
            'debug': s.debug,
            'log_filename': s.log_filename,
            'log_level': s.log_level,
            'user': s.user,
        }

        main(s.argv)

        accent_logging.setup_logging.assert_called_once_with(s.log_filename, debug=s.debug, log_level=s.log_level)

    def test_main_when_config_user_then_change_user(self, load_config, _, __, change_user, *___):
        load_config.return_value = {
            'debug': s.debug,
            'log_filename': s.log_filename,
            'log_level': s.log_level,
            'user': s.user,
        }

        main(s.argv)

        change_user.assert_called_once_with(s.user)

    def test_main_when_no_config_user_then_dont_change_user(self, load_config, _, __, change_user, *___):
        load_config.return_value = {
            'debug': s.debug,
            'log_filename': s.log_filename,
            'log_level': s.log_level,
            'user': None,
        }

        main(s.argv)

        assert_that(change_user.call_count, equal_to(0))

    def test_main_calls_controller_run(self, load_config, controller_init, *_):
        controller = controller_init.return_value
        load_config.return_value = {
            'debug': s.debug,
            'log_filename': s.log_filename,
            'log_level': s.log_level,
            'user': None,
        }

        main(s.argv)

        controller.run.assert_called_once_with()
