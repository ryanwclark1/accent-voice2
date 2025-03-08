# Copyright 2023 Accent Communications

import logging
import sys

import accent_dao
from accent.accent_logging import setup_logging, silence_loggers
from accent.config_helper import set_accent_uuid
from accent.user_rights import change_user

from accent_call_logd.config import load as load_config
from accent_call_logd.controller import Controller
from accent_call_logd.database import database

logger = logging.getLogger(__name__)


def main():
    argv = sys.argv[1:]
    config = load_config(argv)

    if config['user']:
        change_user(config['user'])

    setup_logging(
        config['logfile'], debug=config['debug'], log_level=config['log_level']
    )
    silence_loggers(['amqp'], level=logging.WARNING)

    if config["db_upgrade_on_startup"]:
        database.upgrade(config["db_uri"])

    accent_dao.init_db_from_config({'db_uri': config['cel_db_uri']})
    set_accent_uuid(config, logger)

    controller = Controller(config)
    controller.run()


def upgrade_db():
    conf = load_config(sys.argv[1:])
    database.upgrade(conf["db_uri"])
