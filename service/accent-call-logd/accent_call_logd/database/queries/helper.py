# Copyright 2023 Accent Communications

from contextlib import contextmanager

from ..helpers import wait_is_ready
from .base import BaseDAO


class HelperDAO(BaseDAO):
    @contextmanager
    def db_ready(self):
        with self.new_session() as session:
            wait_is_ready(session)
            yield
