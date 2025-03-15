# src/accent_chatd/dao/channel.py

from typing import Optional
from sqlalchemy import and_, select, text

from accent_chatd.models import Channel
from .base import BaseDAO


class ChannelDAO(BaseDAO):
    async def find(self, name: str) -> Optional[Channel]:
        async with self.session() as session:
            result = await session.execute(select(Channel).filter(Channel.name == name))
            return result.scalars().first()

    async def update(self, channel: Channel) -> Channel:
        async with self.session() as session:
            async with session.begin():
                session.add(channel)
                return channel

    async def delete_all(self) -> None:
        async with self.session() as session:
            async with session.begin():
                await session.execute(text("DELETE FROM chatd_channel"))
