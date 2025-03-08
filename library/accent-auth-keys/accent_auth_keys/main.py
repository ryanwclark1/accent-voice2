# Copyright 2023 Accent Communications

import os
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager
from accent_auth_client import Client

from . import config
from .file_manager import FileManager


class AccentAuthKeys(App):
    DEFAULT_VERBOSE_LEVEL = 0

    def __init__(self):
        super().__init__(
            description='A wrapper to accent-auth-cli to manage internal users',
            command_manager=CommandManager('accent_auth_keys.commands'),
            version='1.0.0',
        )
        self._token = None
        self._client = None

    def build_option_parser(self, *args, **kwargs):
        parser = super().build_option_parser(*args, **kwargs)
        parser.add_argument(
            '--accent-auth-cli-config',
            default=os.getenv('ACCENT_AUTH_CLI_CONFIG', '/root/.config/accent-auth-cli'),
            help='Extra configuration directory to override the accent-auth-cli configuration',
        )
        parser.add_argument(
            '--base-dir',
            default='/var/lib/accent-auth-keys',
            help='The base directory of the file keys',
        )
        parser.add_argument(
            '--config',
            default='/etc/accent-auth-keys',
            help='The accent-auth-keys configuration directory',
        )
        return parser

    @property
    def client(self):
        if not self._client:
            self._client = Client(**self._auth_config)

        if not self._token:
            self._token = self._client.token.new('accent_user', expiration=600)['token']

        self._client.set_token(self._token)
        return self._client

    def initialize_app(self, argv):
        self.LOG.debug('accent-auth-keys')
        self.LOG.debug('options=%s', self.options)

        conf = config.build(self.options)
        self.LOG.debug('Starting with config: %s', conf)

        self.LOG.debug('client args: %s', conf['auth'])
        self._auth_config = dict(conf['auth'])

        self.services = config.load_services(self.options)
        self.file_manager = FileManager(self, self.options.base_dir)


def main(argv=sys.argv[1:]):
    app = AccentAuthKeys()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
