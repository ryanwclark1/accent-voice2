# src/accent_chatd/dao/base.py
from sqlalchemy.ext.asyncio import async_sessionmaker


class BaseDAO:
    def __init__(self, session_maker: async_sessionmaker):
        self._session_maker = session_maker

    @property
    def session(self):
        return self._session_maker
