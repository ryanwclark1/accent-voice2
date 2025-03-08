# Copyright 2023 Accent Communications

from sqlalchemy import and_, text
from sqlalchemy.orm import joinedload

from ...exceptions import UnknownRefreshTokenException
from ..models import RefreshToken


class RefreshTokenDAO:
    def __init__(self, session):
        self._session = session

    @property
    def session(self):
        return self._session()

    def get(self, user_uuid, client_id):
        refresh_token = self.session.query(RefreshToken).get((client_id, user_uuid))
        if not refresh_token:
            raise UnknownRefreshTokenException(client_id, user_uuid)
        return refresh_token

    def find(self, user_uuid, client_id):
        return self._find_by(user_uuid=user_uuid, client_id=client_id)

    def _find_by(self, **kwargs):
        filter_ = text('true')

        if 'user_uuid' in kwargs:
            filter_ = and_(filter_, RefreshToken.user_uuid == kwargs['user_uuid'])
        if 'client_id' in kwargs:
            filter_ = and_(filter_, RefreshToken.client_id == kwargs['client_id'])

        return self.session.query(RefreshToken).filter(filter_).first()

    def list_(self):
        return self.session.query(RefreshToken).options(joinedload('user')).all()

    def update(self, refresh_token):
        self.session.add(refresh_token)
        self.session.flush()
