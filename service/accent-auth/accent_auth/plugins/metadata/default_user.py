# Copyright 2023 Accent Communications

import logging

from accent_auth import BaseMetadata

logger = logging.getLogger(__name__)


class DefaultUser(BaseMetadata):
    def get_token_metadata(self, login, args):
        default_metadata = super().get_token_metadata(login, args)
        metadata = {
            'uuid': default_metadata['uuid'],
            'tenant_uuid': default_metadata['tenant_uuid'],
            'auth_id': default_metadata['auth_id'],
            'pbx_user_uuid': default_metadata['uuid'],
            'accent_uuid': default_metadata['accent_uuid'],
            'purpose': 'user',
        }
        return metadata
