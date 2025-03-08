# Copyright 2023 Accent Communications

# import asyncio
# import uvloop
import logging

from accent import accent_logging
from accent.config_helper import set_accent_uuid
from accent.user_rights import change_user

from accent_websocketd.config import load_config
from accent_websocketd.controller import Controller

logger = logging.getLogger(__name__)


def main():
    # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    config = load_config()

    accent_logging.setup_logging(
        config['log_file'], debug=config['debug'], log_level=config['log_level']
    )
    accent_logging.silence_loggers(['urllib3'], logging.WARNING)
    accent_logging.silence_loggers(['aioamqp'], logging.WARNING)
    set_accent_uuid(config, logger)

    if config['user']:
        change_user(config['user'])

    controller = Controller(config)
    controller.run()
