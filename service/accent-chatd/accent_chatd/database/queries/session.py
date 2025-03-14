# Copyright 2023 Accent Communications

from sqlalchemy import and_, text
from sqlalchemy.orm import joinedload

from ...exceptions import UnknownSessionException
from ..models import Session


class SessionDAO:
    def __init__(self, session):
        self._session = session

    @property
    def session(self):
        return self._session()

    def get(self, session_uuid):
        session = self._find_by(uuid=session_uuid)
        if not session:
            raise UnknownSessionException(session_uuid)
        return session

    def find(self, session_uuid):
        return self._find_by(uuid=session_uuid)

    def _find_by(self, **kwargs):
        filter_ = text('true')

        if 'uuid' in kwargs:
            filter_ = and_(filter_, Session.uuid == kwargs['uuid'])

        return self.session.query(Session).filter(filter_).first()

    def list_(self):
        return self.session.query(Session).options(joinedload('user')).all()

    def update(self, session):
        self.session.add(session)
        self.session.flush()
