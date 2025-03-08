# Copyright 2023 Accent Communications

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import exc
from sqlalchemy.orm import Session as BaseSession
from sqlalchemy.orm import scoped_session

from accent_call_logd.exceptions import DatabaseServiceUnavailable


class BaseDAO:
    def __init__(self, Session: scoped_session):
        self._Session = Session

    @contextmanager
    def new_session(self) -> Iterator[BaseSession]:
        session = self._Session()
        try:
            yield session
            session.commit()
        except exc.OperationalError:
            session.rollback()
            raise DatabaseServiceUnavailable()
        except BaseException:
            session.rollback()
            raise
        finally:
            self._Session.remove()
