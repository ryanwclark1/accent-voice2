# Copyright 2023 Accent Communications

import logging
import sys

from accent import accent_logging
from accent.config_helper import UUIDNotFound, set_accent_uuid
from accent.user_rights import change_user

from accent_confd.config import load as load_config
from accent_confd.controller import Controller

logger = logging.getLogger(__name__)


def main(argv=None):
    argv = argv or sys.argv[1:]
    config = load_config(argv)

    accent_logging.setup_logging(
        config['log_filename'],
        debug=config['debug'],
        log_level=config['log_level'],
    )
    accent_logging.silence_loggers(['Flask-Cors'], logging.WARNING)
    accent_logging.silence_loggers(['amqp'], logging.INFO)

    if config['user']:
        change_user(config['user'])

    try:
        set_accent_uuid(config, logger)
    except UUIDNotFound:
        if config['service_discovery']['enabled']:
            raise

    controller = Controller(config)
    controller.run()
