# Copyright 2023 Accent Communications

from accent.auth_verifier import required_acl
from flask import request
from jsonpatch import JsonPatch

from accent_auth.http import AuthResource, required_top_tenant

from .schemas import config_patch_schema


class ConfigResource(AuthResource):
    def __init__(self, config_service):
        self._config_service = config_service

    @required_acl('auth.config.read')
    @required_top_tenant()
    def get(self):
        return self._config_service.get_config(), 200

    @required_acl('auth.config.update')
    @required_top_tenant()
    def patch(self):
        config_patch = config_patch_schema.load(request.get_json(), many=True)
        config = self._config_service.get_config()
        patched_config = JsonPatch(config_patch).apply(config)
        self._config_service.update_config(patched_config)
        return self._config_service.get_config(), 200
