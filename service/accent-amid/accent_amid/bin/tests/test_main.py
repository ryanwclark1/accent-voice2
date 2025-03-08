# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import Mock, patch

from accent.chain_map import ChainMap

from accent_amid.bin.daemon import main

USER = 'accent-amid'

default_config = {
    'logfile': 'default_logfile',
    'debug': False,
}


class TestMain(TestCase):
    def setUp(self):
        self.log_patch = patch('accent_amid.bin.daemon.setup_logging')
        self.user_patch = patch('accent_amid.bin.daemon.change_user')
        self.set_accent_uuid = patch('accent_amid.bin.daemon.set_accent_uuid')

        self.log = self.log_patch.start()
        self.change_user = self.user_patch.start()
        self.set_accent_uuid = self.set_accent_uuid.start()

    def tearDown(self):
        self.user_patch.stop()
        self.log_patch.stop()
        self.set_accent_uuid.stop()

    @patch(
        'accent_amid.bin.daemon.load_config',
        Mock(return_value=ChainMap({'user': 'foobar'}, default_config)),
    )
    @patch('accent_amid.bin.daemon.Controller', Mock())
    def test_when_arg_user_is_given_then_change_user(self):
        main()

        self.change_user.assert_called_once_with('foobar')
