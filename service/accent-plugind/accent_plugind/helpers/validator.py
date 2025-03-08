# Copyright 2023 Accent Communications

import logging
import re

from marshmallow import ValidationError

from accent_plugind.db import PluginDB
from accent_plugind.exceptions import (
    PluginAlreadyInstalled,
    PluginValidationException,
)
from accent_plugind.schema import PluginMetadataSchema as _PluginMetadataSchema

logger = logging.getLogger(__name__)


class Validator:
    valid_namespace = re.compile(r'^[a-z0-9]+$')
    valid_name = re.compile(r'^[a-z0-9-]+$')
    required_fields = ['name', 'namespace', 'version']

    def __init__(self, plugin_db, current_accent_version, install_params):
        self._db = plugin_db
        self._current_accent_version = current_accent_version
        self._install_params = install_params

        class PluginMetadataSchema(_PluginMetadataSchema):
            current_version = self._current_accent_version

        self._PluginMetadataSchema = PluginMetadataSchema

    def validate(self, metadata):
        logger.debug('Using current version %s', self._current_accent_version)
        logger.debug(
            'max_accent_version: %s', metadata.get('max_accent_version', 'undefined')
        )

        try:
            body = self._PluginMetadataSchema().load(metadata)
        except ValidationError as e:
            raise PluginValidationException(e.messages)
        logger.debug('validated metadata: %s', body)

        if self._install_params['reinstall']:
            return

        if self._db.is_installed(
            metadata['namespace'], metadata['name'], metadata['version']
        ):
            raise PluginAlreadyInstalled(metadata['namespace'], metadata['name'])

    @classmethod
    def new_from_config(cls, config, current_accent_version, install_params):
        plugin_db = PluginDB(config)
        return cls(plugin_db, current_accent_version, install_params)
