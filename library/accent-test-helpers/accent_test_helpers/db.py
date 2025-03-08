# Copyright 2023 Accent Communications
from __future__ import annotations

import logging
from typing import Any

import sqlalchemy
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)


class DBUserClient:
    @classmethod
    def build(
        cls, user: str, password: str, host: str, port: int | str, db: str | None = None
    ) -> DBUserClient:
        return cls(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    def __init__(self, db_uri: str) -> None:
        self._db_uri = db_uri
        self._engine = sqlalchemy.create_engine(self._db_uri)

    def is_up(self) -> bool:
        try:
            self._engine.connect()
            return True
        except Exception as e:
            logger.debug('Database is down: %s', e)
            return False

    def execute(self, query: str, **kwargs: Any) -> None:
        with self._engine.connect() as connection:
            connection.execute(text(query), **kwargs)
