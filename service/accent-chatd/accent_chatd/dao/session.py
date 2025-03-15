# src/accent_chatd/dao/session.py

from typing import List, Optional

from sqlalchemy import and_, select, text
from sqlalchemy.orm import joinedload

from accent_chatd.exceptions import UnknownSessionException
from accent_chatd.models import Session
from .base import BaseDAO


class SessionDAO(BaseDAO):
    async def get(self, session_uuid: str) -> Session:
        async with self.session() as session:
            stmt = select(Session).where(Session.uuid == session_uuid)
            result = await session.execute(stmt)
            ses = result.scalars().first()
            if not ses:
                raise UnknownSessionException(session_uuid)
            return ses

    async def find(self, session_uuid: str) -> Optional[Session]:
        async with self.session() as session:
            stmt = select(Session).where(Session.uuid == session_uuid)
            result = await session.execute(stmt)
            return result.scalars().first()

    async def list_(self) -> List[Session]:
        async with self.session() as session:
            result = await session.execute(
                select(Session).options(joinedload(Session.user))
            )
            return result.scalars().all()

    async def update(self, session: Session) -> Session:
        async with self.session() as session:
            async with session.begin():
                session.add(session)
                return session
