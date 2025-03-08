# Copyright 2023 Accent Communications

import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

from . import config


class AccentDebugApp(App):
    def __init__(self):
        super().__init__(
            description='Accent Debug',
            command_manager=CommandManager('accent_debug.commands'),
            version='1.1.0',
            deferred_help=True,
        )
        self.config = None

    def build_option_parser(self, *args, **kwargs):
        parser = super().build_option_parser(*args, **kwargs)
        parser.add_argument(
            '--config',
            default='/etc/accent-debug',
            help='The accent-debug configuration directory',
        )
        return parser

    def initialize_app(self, argv):
        self.config = config.build(self.options)


def main(argv=sys.argv[1:]):
    myapp = AccentDebugApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
