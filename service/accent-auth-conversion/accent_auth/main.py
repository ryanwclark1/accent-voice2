# Copyright 2023 Accent Communications

import logging
import sys

from accent import accent_logging
from accent.config_helper import UUIDNotFound, set_accent_uuid
from accent.user_rights import change_user

from accent_auth.config import get_config
from accent_auth.controller import Controller
from accent_auth.database import database

SPAMMY_LOGGERS = ['urllib3', 'Flask-Cors', 'amqp', 'kombu']

logger = logging.getLogger(__name__)


def main():
    accent_logging.silence_loggers(SPAMMY_LOGGERS, logging.WARNING)

    config = get_config(sys.argv[1:])

    accent_logging.setup_logging(
        config['log_filename'],
        debug=config['debug'],
        log_level=config['log_level'],
    )

    if config['user']:
        change_user(config['user'])

    if config["db_upgrade_on_startup"]:
        database.upgrade(config["db_uri"])

    try:
        set_accent_uuid(config, logger)
    except UUIDNotFound:
        if config['service_discovery']['enabled']:
            raise

    controller = Controller(config)
    controller.run()


def upgrade_db():
    conf = get_config(sys.argv[1:])
    database.upgrade(conf["db_uri"])
