# Copyright 2023 Accent Communications

import logging

from accent_auth import BaseMetadata

logger = logging.getLogger(__name__)


DEFAULT_ADMIN_POLICY = 'accent_default_admin_policy'
DEFAULT_ADMIN_GROUP = 'accent_default_admin_group'


class UserAdminStatus(BaseMetadata):
    def get_token_metadata(self, login, args):
        metadata = super().get_token_metadata(login, args)
        return {'admin': self._is_admin(metadata['auth_id'])}

    def _is_admin(self, user_uuid):
        service = self._user_service

        has_admin_policy = bool(
            service.list_policies(user_uuid, slug=DEFAULT_ADMIN_POLICY)
        )

        return has_admin_policy or bool(
            service.list_groups(user_uuid, slug=DEFAULT_ADMIN_GROUP)
        )
