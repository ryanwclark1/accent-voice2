# Copyright 2023 Accent Communications

import logging
import threading

from accent_amid.config import AmidConfigDict


class ConfigService:

    # Changing root logger log-level requires application-wide lock.
    # This lock will be shared across all instances.
    _lock = threading.Lock()

    def __init__(self, config: AmidConfigDict) -> None:
        self._config = AmidConfigDict(**config)
        self._enabled = False

    def get_config(self) -> dict:
        with self._lock:
            return dict(self._config)

    def update_config(self, config: dict) -> None:
        with self._lock:
            self._update_debug(config['debug'])
            self._config['debug'] = config['debug']

    def _update_debug(self, debug: bool) -> None:
        if debug:
            self._enable_debug()
        else:
            self._disable_debug()

    def _enable_debug(self) -> None:
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

    def _disable_debug(self) -> None:
        root_logger = logging.getLogger()
        root_logger.setLevel(self._config['log_level'])
