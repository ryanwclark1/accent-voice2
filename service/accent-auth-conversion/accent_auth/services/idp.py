# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import Literal

from accent_auth.database.models import User
from accent_auth.services.helpers import BaseService

IDPType = Literal[
    'default',
    'native',
    'ldap',
    'saml',
]


class IDPService(BaseService):
    def add_user(self, idp_type: IDPType, user_uuid: str) -> User:
        return self._dao.user.update(user_uuid, authentication_method=idp_type)

    def remove_user(self, idp_type: IDPType, user_uuid: str) -> User:
        user = self._dao.user.get(user_uuid)
        if user.authentication_method == idp_type:
            return self.add_user('default', user_uuid)
        return user
