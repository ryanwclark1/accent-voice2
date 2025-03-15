# src/accent_chatd/dao/endpoint.py

from typing import Optional

from sqlalchemy import and_, select, text

from accent_chatd.exceptions import UnknownEndpointException
from accent_chatd.models import Endpoint
from .base import BaseDAO


class EndpointDAO(BaseDAO):
    async def create(self, endpoint: Endpoint) -> Endpoint:
        async with self.session() as session:
            async with session.begin():
                session.add(endpoint)
                await session.flush()
                await session.refresh(endpoint)
                return endpoint

    async def find_by(self, **kwargs) -> Optional[Endpoint]:
        async with self.session() as session:
            stmt = select(Endpoint)
            if "name" in kwargs:
                stmt = stmt.where(Endpoint.name == kwargs["name"])

            result = await session.execute(stmt)
            return result.scalars().first()

    async def get_by(self, **kwargs) -> Endpoint:
        endpoint = await self.find_by(**kwargs)
        if not endpoint:
            raise UnknownEndpointException(kwargs.get("name"))
        return endpoint

    async def find_or_create(self, name: str) -> Endpoint:
        try:
            return await self.get_by(name=name)
        except UnknownEndpointException:
            return await self.create(Endpoint(name=name))

    async def update(self, endpoint: Endpoint) -> Endpoint:
        async with self.session() as session:
            async with session.begin():
                session.add(endpoint)
                return endpoint

    async def delete_all(self) -> None:
        async with self.session() as session:
            async with session.begin():
                await session.execute(text("DELETE FROM chatd_endpoint"))
