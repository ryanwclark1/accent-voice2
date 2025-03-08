# Copyright 2023 Accent Communications

import sys

from accent import accent_logging
from accent.user_rights import change_user

from accent_ui.config import load as load_config
from accent_ui.controller import Controller


def main():
    config = load_config(sys.argv[1:])

    if config.get('user'):
        change_user(config['user'])

    accent_logging.setup_logging(
        config['log_filename'],
        debug=config['debug'],
        log_level=config['log_level'],
    )

    controller = Controller(config)
    controller.run()
