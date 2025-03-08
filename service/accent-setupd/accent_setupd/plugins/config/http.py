# Copyright 2023 Accent Communications

from accent.auth_verifier import required_acl

from accent_setupd.auth import required_master_tenant
from accent_setupd.http import AuthResource


class ConfigResource(AuthResource):
    def __init__(self, config):
        self._config = config

    @required_master_tenant()
    @required_acl('setupd.config.read')
    def get(self):
        return dict(self._config), 200