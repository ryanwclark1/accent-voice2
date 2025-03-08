# Copyright 2023 Accent Communications

import logging
import os

from accent import accent_logging
from accent.config_helper import UUIDNotFound, set_accent_uuid
from accent.user_rights import change_user

from accent_plugind import config
from accent_plugind.controller import Controller
from accent_plugind.root_worker import RootWorker

logger = logging.getLogger(__name__)


def main(args):
    conf = config.load_config(args)

    accent_logging.setup_logging(
        conf['log_file'], debug=conf['debug'], log_level=conf['log_level']
    )

    os.chdir(conf['home_dir'])

    with RootWorker() as root_worker:
        if conf['user']:
            change_user(conf['user'])

        try:
            set_accent_uuid(conf, logger)
        except UUIDNotFound:
            # handled in the controller
            pass

        controller = Controller(conf, root_worker)
        logger.debug('starting')
        controller.run()
        logger.debug('controller stopped')
