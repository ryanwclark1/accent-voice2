# Copyright 2023 Accent Communications

from sqlalchemy import and_, text

from ..models import Channel


class ChannelDAO:
    def __init__(self, session):
        self._session = session

    @property
    def session(self):
        return self._session()

    def find(self, name):
        return self._find_by(name=name)

    def _find_by(self, **kwargs):
        filter_ = text('true')

        if 'name' in kwargs:
            filter_ = and_(filter_, Channel.name == kwargs['name'])

        return self.session.query(Channel).filter(filter_).first()

    def update(self, channel):
        self.session.add(channel)
        self.session.flush()

    def delete_all(self):
        self.session.query(Channel).delete()
        self.session.flush()
