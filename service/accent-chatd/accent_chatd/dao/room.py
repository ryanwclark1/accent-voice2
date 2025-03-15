# src/accent_chatd/dao/room.py

from typing import List, Optional
from sqlalchemy import and_, distinct, func, select, text
from sqlalchemy.dialects.postgresql import array_agg
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from accent_chatd.exceptions import UnknownRoomException
from accent_chatd.models import Room, RoomMessage, RoomUser
from .base import BaseDAO


class unaccent(ReturnTypeFromArgs):  # Keep the unaccent function
    pass


class RoomDAO(BaseDAO):
    async def create(self, room: Room) -> Room:
        async with self.session() as session:
            async with session.begin():
                session.add(room)
                await session.flush()
                await session.refresh(room)
                return room

    async def get(self, tenant_uuids: List[str], room_uuid: str) -> Room:
        async with self.session() as session:
            stmt = (
                select(Room)
                .options(
                    selectinload(Room.users),  # Eager load users and messages
                    selectinload(Room.messages),
                )
                .where(Room.tenant_uuid.in_(tenant_uuids), Room.uuid == room_uuid)
            )
            result = await session.execute(stmt)
            room = result.scalars().first()
            if not room:
                raise UnknownRoomException(room_uuid)
            return room

    async def list_(
        self,
        tenant_uuids: Optional[List[str]] = None,
        user_uuids: Optional[List[str]] = None,
        exact_user_uuids: bool = False,
    ) -> List[Room]:
        async with self.session() as session:
            query = select(Room).options(selectinload(Room.users))

            if user_uuids:
                # Subquery for matching rooms with exact or partial user UUIDs
                subquery = (
                    select(RoomUser.room_uuid)
                    .group_by(RoomUser.room_uuid)
                    .having(
                        and_(
                            array_agg(distinct(RoomUser.uuid)).contains(user_uuids),
                            array_agg(distinct(RoomUser.uuid)).contained_by(user_uuids)
                            if exact_user_uuids
                            else text("TRUE"),
                        )
                    )
                ).subquery()
                query = query.where(Room.uuid.in_(subquery))

            if tenant_uuids is None:
                return (await session.execute(query)).scalars().all()

            if not tenant_uuids:
                query = query.where(
                    text("FALSE")
                )  # No valid tenants, return empty list
            else:
                query = query.where(Room.tenant_uuid.in_(tenant_uuids))
            result = await session.execute(query)
            return result.scalars().all()

    async def count(
        self,
        tenant_uuids: List[str],
        user_uuids: Optional[List[str]] = None,
        exact_user_uuids: bool = False,
    ) -> int:
        async with self.session() as session:
            query = select(func.count(Room.id))
            if user_uuids:
                # Subquery for matching rooms with exact or partial user UUIDs
                subquery = (
                    select(RoomUser.room_uuid)
                    .group_by(RoomUser.room_uuid)
                    .having(
                        and_(
                            array_agg(distinct(RoomUser.uuid)).contains(user_uuids),
                            array_agg(distinct(RoomUser.uuid)).contained_by(user_uuids)
                            if exact_user_uuids
                            else text("TRUE"),
                        )
                    )
                ).subquery()
                query = query.where(Room.uuid.in_(subquery))

            if not tenant_uuids:
                query = query.where(text("false"))  # No valid tenants, return 0.
            else:
                query = query.where(Room.tenant_uuid.in_(tenant_uuids))

            result = await session.execute(query)
            return result.scalar_one()

    async def add_message(self, room: Room, message: RoomMessage) -> None:
        async with self.session() as session:
            async with session.begin():
                room.messages.append(message)

    async def list_messages(self, room: Room, **filter_parameters) -> List[RoomMessage]:
        async with self.session() as session:
            query = self._build_messages_query(room.uuid)
            query = self._list_filter(query, **filter_parameters)
            query = self._paginate(query, **filter_parameters)
            result = await session.execute(query)
            return result.scalars().all()

    async def count_messages(self, room: Room, **filter_parameters) -> int:
        async with self.session() as session:
            query = self._build_messages_query(room.uuid)
            query = self._list_filter(query, **filter_parameters)
            result = await session.execute(
                select(func.count()).select_from(query)
            )  # Count from subquery
            return result.scalar_one()

    def _build_messages_query(self, room_uuid: str):
        return select(RoomMessage).where(RoomMessage.room_uuid == room_uuid)

    async def list_user_messages(
        self, tenant_uuid: str, user_uuid: str, **filter_parameters
    ) -> List[RoomMessage]:
        async with self.session() as session:
            query = self._build_user_messages_query(tenant_uuid, user_uuid)
            query = self._list_filter(query, **filter_parameters)
            query = self._paginate(query, **filter_parameters)
            result = await session.execute(query)
            return result.scalars().all()

    async def count_user_messages(
        self, tenant_uuid: str, user_uuid: str, **filter_parameters
    ) -> int:
        async with self.session() as session:
            query = self._build_user_messages_query(tenant_uuid, user_uuid)
            query = self._list_filter(query, **filter_parameters)
            result = await session.execute(
                select(func.count()).select_from(query)
            )  # Count using subquery.
            return result.scalar_one()

    def _build_user_messages_query(self, tenant_uuid: str, user_uuid: str, *filters):
        return (
            select(RoomMessage)
            .join(Room)
            .join(RoomUser)
            .where(RoomUser.tenant_uuid == tenant_uuid)
            .where(RoomUser.uuid == user_uuid)
        )

    def _paginate(
        self,
        query,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order: str = "created_at",
        direction: str = "desc",
        **ignored,
    ):
        order_column = getattr(RoomMessage, order)
        if direction == "asc":
            order_column = order_column.asc()
        else:
            order_column = order_column.desc()
        query = query.order_by(order_column)

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        return query

    def _list_filter(
        self,
        query,
        search: Optional[str] = None,
        from_date=None,
        distinct=None,
        **ignored,
    ):
        if distinct is not None:
            distinct_field = getattr(RoomMessage, distinct)
            query = (
                query.distinct(distinct_field)
                .order_by(distinct_field, RoomMessage.created_at.desc())
                .from_self()
            )

        if search is not None:
            words = [word for word in search.split(" ") if word]
            pattern = f"%{'%'.join(words)}%"
            query = query.where(unaccent(RoomMessage.content).ilike(pattern))

        if from_date is not None:
            query = query.where(RoomMessage.created_at >= from_date)

        return query
