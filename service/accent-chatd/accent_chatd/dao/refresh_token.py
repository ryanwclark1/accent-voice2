# src/accent_chatd/dao/refresh_token.py

from typing import List, Optional

from sqlalchemy import and_, select, text
from sqlalchemy.orm import joinedload

from accent_chatd.exceptions import UnknownRefreshTokenException
from accent_chatd.models import RefreshToken

from .base import BaseDAO


class RefreshTokenDAO(BaseDAO):
    async def get(self, user_uuid: str, client_id: str) -> RefreshToken:
        async with self.session() as session:
            result = await session.execute(
                select(RefreshToken).filter_by(client_id=client_id, user_uuid=user_uuid)
            )
            refresh_token = result.scalars().first()
            if not refresh_token:
                raise UnknownRefreshTokenException(client_id, user_uuid)
            return refresh_token

    async def find(self, user_uuid: str, client_id: str) -> Optional[RefreshToken]:
        async with self.session() as session:
            result = await session.execute(
                select(RefreshToken).filter_by(user_uuid=user_uuid, client_id=client_id)
            )
            return result.scalars().first()

    async def list_(self) -> List[RefreshToken]:
        async with self.session() as session:
            result = await session.execute(
                select(RefreshToken).options(joinedload(RefreshToken.user))
            )
            return result.scalars().all()

    async def update(self, refresh_token: RefreshToken) -> RefreshToken:
        async with self.session() as session:
            async with session.begin():
                session.add(refresh_token)
                return refresh_token