# accent_auth/services/idp.py

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

# from accent_auth.services.helpers import BaseService  # REMOVED
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from accent_auth.db import DAO

IDPType = Literal[
    "default",
    "native",
    "ldap",
    "saml",
]  # Keep this, it's a good way to define the valid types


class IDPService:  # Removed inheritance
    def __init__(self, dao: DAO):
        self._dao = dao

    async def add_user(
        self, idp_type: IDPType, user_uuid: str, db: AsyncSession
    ) -> None:
        """Associates a user with an IDP type."""
        await self._dao.user.update(
            user_uuid, authentication_method=idp_type, session=db
        )

    async def remove_user(
        self, idp_type: IDPType, user_uuid: str, db: AsyncSession
    ) -> None:
        """Removes the association between a user and an IDP type."""
        user = await self._dao.user.get(user_uuid, session=db)
        if user and user.authentication_method == idp_type:
            await self._dao.user.update(
                user_uuid, authentication_method="default", session=db
            )

    async def list(self, db: AsyncSession = None) -> list[IDPType]:
        return ["default", "native", "ldap", "saml"]
