# Copyright 2023 Accent Communications

from __future__ import annotations

import logging
import signal
from functools import partial
from types import FrameType

from accent.accent_logging import setup_logging
from accent.config_helper import set_accent_uuid
from accent.user_rights import change_user

from accent_amid.config import load_config
from accent_amid.controller import Controller

logger = logging.getLogger(__name__)


def main() -> None:
    config = load_config()

    setup_logging(config['logfile'], debug=config['debug'])

    if config.get('user'):
        change_user(config['user'])

    set_accent_uuid(config, logger)

    controller = Controller(config)
    signal.signal(signal.SIGTERM, partial(_signal_handler, controller))
    signal.signal(signal.SIGINT, partial(_signal_handler, controller))

    controller.run()


def _signal_handler(controller: Controller, signum: int, frame: FrameType) -> None:
    controller.stop(reason=signal.Signals(signum).name)


if __name__ == '__main__':
    main()
