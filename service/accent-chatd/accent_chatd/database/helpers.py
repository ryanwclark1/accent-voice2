# Copyright 2023 Accent Communications

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

Session = scoped_session(sessionmaker())


def init_db(db_uri, echo=False, pool_size=16):
    engine = create_engine(db_uri, echo=echo, pool_size=pool_size, pool_pre_ping=True)
    Session.configure(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        Session.remove()
