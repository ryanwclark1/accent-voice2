# Copyright 2023 Accent Communications

from __future__ import annotations

import logging
from typing import Any

_logger = logging.getLogger(__name__)


def setup_logging() -> None:
    formatter = logging.Formatter('[%(asctime)s] %(message)s')
    handler = logging.FileHandler('/var/log/accent-provd-fail2ban.log')
    handler.setFormatter(formatter)
    _logger.addHandler(handler)


def log_security_msg(msg: str, *args: Any) -> None:
    _logger.info(msg, *args)
