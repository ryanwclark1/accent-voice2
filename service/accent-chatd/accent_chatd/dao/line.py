# src/accent_chatd/dao/line.py
from typing import Optional, List
from sqlalchemy import and_, select, text

from accent_chatd.exceptions import UnknownLineException
from accent_chatd.models import Line, Endpoint, Channel
from .base import BaseDAO


class LineDAO(BaseDAO):
    async def get(self, line_id: int) -> Line:
        async with self.session() as session:
            stmt = select(Line).where(Line.id == line_id)
            result = await session.execute(stmt)
            line = result.scalars().first()
            if not line:
                raise UnknownLineException(line_id)
            return line

    async def find(self, line_id: int) -> Optional[Line]:
        async with self.session() as session:
            stmt = select(Line).where(Line.id == line_id)
            result = await session.execute(stmt)
            return result.scalars().first()

    async def find_by(self, **kwargs) -> Optional[Line]:
        async with self.session() as session:
            stmt = select(Line)
            if "id" in kwargs:
                stmt = stmt.where(Line.id == kwargs["id"])
            if "endpoint_name" in kwargs:
                stmt = stmt.where(Line.endpoint_name == kwargs["endpoint_name"])

            result = await session.execute(stmt)
            return result.scalars().first()

    async def list_(self) -> List[Line]:
        async with self.session() as session:
            result = await session.execute(select(Line))
            return result.scalars().all()

    async def update(self, line: Line) -> Line:
        async with self.session() as session:
            async with session.begin():
                session.add(line)
                return line

    async def associate_endpoint(self, line: Line, endpoint: Endpoint) -> None:
        async with self.session() as session:
            async with session.begin():
                line.endpoint = endpoint

    async def dissociate_endpoint(self, line: Line) -> None:
        async with self.session() as session:
            async with session.begin():
                line.endpoint = None

    async def add_channel(self, line: Line, channel: Channel) -> None:
        async with self.session() as session:
            async with session.begin():
                if channel not in line.channels:
                    line.channels.append(channel)

    async def remove_channel(self, line: Line, channel: Channel) -> None:
        async with self.session() as session:
            async with session.begin():
                if channel in line.channels:
                    line.channels.remove(channel)
