# Copyright 2023 Accent Communications

import logging
import threading


class ConfigService:
    # Changing root logger log-level requires application-wide lock.
    # This lock will be shared across all instances.
    _lock = threading.Lock()

    def __init__(self, config):
        self._config = dict(config)

    def get(self):
        return self._config

    def update_config(self, config):
        with self._lock:
            self._update_debug(config['debug'])
            self._config['debug'] = config['debug']

    def _update_debug(self, debug):
        if debug:
            self._enable_debug()
        else:
            self._disable_debug()

    def _enable_debug(self):
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

    def _disable_debug(self):
        root_logger = logging.getLogger()
        root_logger.setLevel(self._config['log_level'])
