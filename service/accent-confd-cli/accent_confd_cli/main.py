# Copyright 2023 Accent Communications

import logging
import os
import os.path
import sys

from accent_confd_client import Client
from cliff.app import App
from cliff.commandmanager import CommandManager

from . import config

logging.getLogger('requests').setLevel(logging.ERROR)


class AccentConfdCLI(App):
    DEFAULT_VERBOSE_LEVEL = 0

    def __init__(self):
        super().__init__(
            description='A CLI for the accent-confd service',
            command_manager=CommandManager('accent_confd_cli.commands'),
            version='0.0.1',
        )
        self._current_token = None
        self._remove_token = False
        self._client = None
        self._backend = None

    def build_option_parser(self, *args, **kwargs):
        parser = super().build_option_parser(*args, **kwargs)
        config_path_from_env = os.getenv('ACCENT_CONFD_CLI_CONFIG', None)
        config_path_default = os.path.expanduser(
            os.path.join('~', '.config', 'accent-confd-cli')
        )
        parser.add_argument(
            '--config',
            default=(config_path_from_env or config_path_default),
            help='Extra configuration directory to override the system configuration',
        )
        parser.add_argument('--hostname', help='The accent-confd hostname')
        parser.add_argument('--port', help='The accent-confd port')
        parser.add_argument(
            '--prefix', help='The URL prefix to use to reach accent-confd'
        )
        parser.add_argument('--token', required=True, help='The accent-auth token to use')

        https_verification = parser.add_mutually_exclusive_group()
        https_verification.add_argument(
            '--ssl', dest='https', action='store_true', help="Use ssl"
        )
        https_verification.add_argument(
            '--no-ssl', dest='https', action='store_false', help="Don't use ssl"
        )

        certificate_options = parser.add_mutually_exclusive_group()
        certificate_options.add_argument(
            '--verify', action='store_true', help='Verify the HTTPS certificate or not'
        )
        certificate_options.add_argument(
            '--insecure', action='store_true', help='Bypass certificate verification'
        )
        certificate_options.add_argument('--cacert', help='Specify the ca bundle file')

        return parser

    @property
    def client(self):
        if not self._client:
            self._client = Client(**self._confd_config)

        return self._client

    def initialize_app(self, argv):
        self.LOG.debug('Accent Confd CLI')
        self.LOG.debug('options=%s', self.options)
        conf = config.build(self.options)
        self.LOG.debug('Starting with config: %s', conf)
        self._current_token = self.options.token

        self.LOG.debug('client args: %s', conf['confd'])
        self._confd_config = dict(conf['confd'])


def main(argv=sys.argv[1:]):
    app = AccentConfdCLI()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
