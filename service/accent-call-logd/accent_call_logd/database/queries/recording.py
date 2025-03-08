# Copyright 2023 Accent Communications

from ..models import Recording
from .base import BaseDAO


class _UselessQuery(Exception):
    pass


class RecordingDAO(BaseDAO):
    def delete_media_by(self, **kwargs):
        with self.new_session() as session:
            query = session.query(Recording)
            try:
                query = self._apply_filters(query, kwargs)
            except _UselessQuery:
                return

            recordings = query.all()
            for recording in recordings:
                recording.path = None
                session.flush()
                session.expunge(recording)

    def find_by(self, **kwargs):
        with self.new_session() as session:
            query = session.query(Recording)
            try:
                query = self._apply_filters(query, kwargs)
            except _UselessQuery:
                return

            recording = query.first()
            if not recording:
                return
            session.expunge(recording)
            return recording

    def _apply_filters(self, query, params):
        if 'call_log_ids' in params:
            if not params['call_log_ids']:
                raise _UselessQuery()
            query = query.filter(Recording.call_log_id.in_(params['call_log_ids']))

        if 'call_log_id' in params:
            query = query.filter(Recording.call_log_id == params['call_log_id'])

        if 'uuid' in params:
            query = query.filter(Recording.uuid == params['uuid'])

        return query
