# Copyright 2023 Accent Communications

from contextlib import contextmanager

from accent_dao.helpers import db_manager
from accent_dao.helpers.db_manager import daosession


@contextmanager
def flush_session(session):
    try:
        yield
        session.flush()
    except Exception:
        session.rollback()
        raise


@daosession
def get_dao_session(session):
    return session


@contextmanager
def session_scope(read_only=False):
    session = db_manager.Session()
    try:
        yield session
        if not read_only:
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        db_manager.Session.remove()
