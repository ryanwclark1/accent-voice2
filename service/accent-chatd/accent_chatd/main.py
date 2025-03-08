# Copyright 2023 Accent Communications

import logging
import sys

from accent import accent_logging
from accent.config_helper import set_accent_uuid
from accent.user_rights import change_user

from accent_chatd import config
from accent_chatd.controller import Controller

logger = logging.getLogger(__name__)


def main():
    conf = config.load_config(sys.argv[1:])

    if conf['user']:
        change_user(conf['user'])

    accent_logging.setup_logging(
        conf['log_file'], debug=conf['debug'], log_level=conf['log_level']
    )
    accent_logging.silence_loggers(
        ['Flask-Cors', 'urllib3', 'stevedore.extension', 'amqp'], logging.WARNING
    )

    set_accent_uuid(conf, logger)

    controller = Controller(conf)
    controller.run()
