# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

from accent.auth_verifier import required_acl
from flask import request
from jsonpatch import JsonPatch

from accent_webhookd.auth import required_master_tenant
from accent_webhookd.rest_api import AuthResource

from .schemas import config_patch_schema

if TYPE_CHECKING:
    from ...types import WebhookdConfigDict
    from .service import ConfigService


class ConfigResource(AuthResource):
    def __init__(self, config_service: ConfigService) -> None:
        self._config_service = config_service

    @required_master_tenant()
    @required_acl('webhookd.config.read')
    def get(self) -> tuple[WebhookdConfigDict, int]:
        return self._config_service.get_config(), 200

    @required_master_tenant()
    @required_acl('webhookd.config.update')
    def patch(self) -> tuple[WebhookdConfigDict, int]:
        config_patch = config_patch_schema.load(request.get_json(), many=True)
        config = self._config_service.get_config()
        patched_config = JsonPatch(config_patch).apply(config)
        self._config_service.update_config(patched_config)
        return self._config_service.get_config(), 200
