# Copyright 2023 Accent Communications

import logging

from accent_auth_client import Client as AuthClient

from accent_auth import BaseMetadata, helpers

logger = logging.getLogger(__name__)


class Plugin(BaseMetadata):
    def load(self, dependencies):
        super().load(dependencies)
        self._token_service = dependencies['token_service']
        self.token_renewer = helpers.LocalTokenRenewer(
            self._token_service, acl=['test.internal_token']
        )

    def get_token_metadata(self, login, args):
        metadata = super().get_token_metadata(login, args)

        token = self.token_renewer.get_token()
        client = AuthClient(host='auth', port=9497, https=False, prefix=None)
        is_valid = client.token.is_valid(
            token, tenant=self._token_service.top_tenant_uuid
        )

        metadata['internal_token_is_valid'] = is_valid
        return metadata
