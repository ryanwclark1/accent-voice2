# src/accent_chatd/dao/user.py


from sqlalchemy import func, select, text
from sqlalchemy.orm import selectinload

from accent_chatd.exceptions import UnknownUserException
from accent_chatd.models import User

from .base import BaseDAO


class UserDAO(BaseDAO):
    async def create(self, user: User) -> User:
        async with self.session() as session:
            async with session.begin():
                session.add(user)
                await session.flush()  # Ensure any server-side defaults are populated
                await session.refresh(user)
                return user

    async def update(self, user: User) -> User:
        async with self.session() as session:
            async with session.begin():
                session.add(user)
                return user

    async def get(self, tenant_uuids: list[str], user_uuid: str) -> User:
        async with self.session() as session:
            # Use selectinload to eager load relationships.
            stmt = (
                select(User)
                .options(
                    selectinload(User.sessions),
                    selectinload(User.lines),
                    selectinload(User.refresh_tokens),
                )
                .where(User.tenant_uuid.in_(tenant_uuids), User.uuid == user_uuid)
            )
            result = await session.execute(stmt)
            user = result.scalars().first()  # Use .first() for one-or-none semantics
            if not user:
                raise UnknownUserException(user_uuid)
            return user

    async def list_(
        self,
        tenant_uuids: list[str] | None = None,
        uuids: list[str] | None = None,
    ) -> list[User]:
        async with self.session() as session:
            stmt = select(User).options(
                selectinload(User.sessions),
                selectinload(User.lines),
                selectinload(User.refresh_tokens),
            )  # Eager load related entities
            if uuids:
                stmt = stmt.where(User.uuid.in_(uuids))
            if tenant_uuids is not None:
                if not tenant_uuids:
                    stmt = stmt.where(
                        text("false")
                    )  # No valid tenants, return empty list
                else:
                    stmt = stmt.where(User.tenant_uuid.in_(tenant_uuids))

            result = await session.execute(stmt)
            return result.scalars().all()

    async def count(
        self, tenant_uuids: list[str] | None = None, **filter_parameters
    ) -> int:
        async with self.session() as session:
            stmt = select(func.count(User.id))
            if tenant_uuids is not None:
                if not tenant_uuids:
                    stmt = stmt.where(text("false"))  # No valid tenants, return 0
                else:
                    stmt = stmt.where(User.tenant_uuid.in_(tenant_uuids))

            result = await session.execute(stmt)
            return result.scalar_one()

    async def delete(self, user: User) -> None:
        async with self.session() as session:
            async with session.begin():
                await session.delete(user)

    # User relationships
    async def add_session(self, user: User, session_obj: Session) -> None:
        async with self.session() as session:
            async with session.begin():
                if session_obj not in user.sessions:
                    user.sessions.append(session_obj)

    async def remove_session(self, user: User, session_obj: Session) -> None:
        async with self.session() as session:
            async with session.begin():
                if session_obj in user.sessions:
                    user.sessions.remove(session_obj)

    async def add_line(self, user: User, line: Line) -> None:
        async with self.session() as session:
            async with session.begin():
                if line not in user.lines:
                    user.lines.append(line)

    async def remove_line(self, user: User, line: Line) -> None:
        async with self.session() as session:
            async with session.begin():
                if line in user.lines:
                    user.lines.remove(line)

    async def add_refresh_token(self, user: User, refresh_token: RefreshToken) -> None:
        async with self.session() as session:
            async with session.begin():
                if refresh_token not in user.refresh_tokens:
                    user.refresh_tokens.append(refresh_token)

    async def remove_refresh_token(
        self, user: User, refresh_token: RefreshToken
    ) -> None:
        async with self.session() as session:
            async with session.begin():
                if refresh_token in user.refresh_tokens:
                    user.refresh_tokens.remove(refresh_token)
