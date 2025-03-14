# Copyright 2023 Accent Communications

import time
import uuid

from hamcrest import (
    all_of,
    assert_that,
    contains_exactly,
    empty,
    equal_to,
    has_entries,
    has_items,
    has_properties,
    not_,
)

from accent_auth import exceptions
from accent_auth.database import models

from .helpers import base, fixtures

SESSION_UUID_1 = str(uuid.uuid4())


@base.use_asset('database')
class TestTokenDAO(base.DAOTestCase):
    def _get_token_body(self):
        now = int(time.time())
        return {
            'auth_id': 'test',
            'pbx_user_uuid': str(uuid.uuid4),
            'accent_uuid': str(uuid.uuid4),
            'issued_t': now,
            'expire_t': now + 120,
            'acl': ['first', 'second'],
            'metadata': {
                'uuid': '08b213da-9963-4d25-96a3-f02d717e82f2',
                'id': 42,
                'msg': 'a string field',
            },
            'user_agent': 'my-user-agent',
            'remote_addr': '192.168.1.1',
        }

    @fixtures.db.refresh_token()
    def test_create(self, refresh_token_uuid):
        body = self._get_token_body()
        session = {}
        token_uuid, session_uuid = self._token_dao.create(body, session)

        result = self._token_dao.get(token_uuid)
        assert_that(
            result, has_entries(uuid=token_uuid, session_uuid=session_uuid, **body)
        )

        refresh_body = self._get_token_body()
        token_uuid, session_uuid = self._token_dao.create(
            {'refresh_token_uuid': refresh_token_uuid, **refresh_body},
            session,
        )
        result = self._token_dao.get(token_uuid)
        assert_that(
            result,
            has_entries(
                uuid=token_uuid,
                session_uuid=session_uuid,
                **refresh_body,
            ),
        )

    @fixtures.db.token()
    @fixtures.db.token()
    @fixtures.db.token()
    def test_get(self, token, *_):
        self.assertRaises(
            exceptions.UnknownTokenException, self._token_dao.get, 'unknown'
        )
        result = self._token_dao.get(token['uuid'])
        assert_that(result, equal_to(token))

    @fixtures.db.token()
    def test_delete(self, token):
        self._token_dao.delete(token['uuid'])
        self.assertRaises(
            exceptions.UnknownTokenException, self._token_dao.get, token['uuid']
        )
        self._token_dao.delete(token['uuid'])  # No error on delete unknown

    @fixtures.db.token()
    @fixtures.db.token(expiration=0)
    @fixtures.db.token(expiration=0)
    def test_delete_expired_tokens_and_sessions(self, token_1, token_2, token_3):
        expired_tokens, expired_sessions = next(
            self._token_dao.purge_expired_tokens_and_sessions()
        )

        assert_that(
            expired_tokens,
            all_of(
                not_(has_items(has_entries(uuid=token_1['uuid']))),
                has_items(has_entries(uuid=token_2['uuid'])),
                has_items(has_entries(uuid=token_3['uuid'])),
            ),
        )

        assert_that(
            expired_sessions,
            all_of(
                not_(has_items(has_entries(uuid=token_1['session_uuid']))),
                has_items(has_entries(uuid=token_2['session_uuid'])),
                has_items(has_entries(uuid=token_3['session_uuid'])),
            ),
        )

        sessions = self.session.query(models.Session).all()
        assert_that(
            sessions,
            all_of(
                has_items(has_properties(uuid=token_1['session_uuid'])),
                not_(has_items(has_properties(uuid=token_2['session_uuid']))),
                not_(has_items(has_properties(uuid=token_3['session_uuid']))),
            ),
        )

        tokens = self.session.query(models.Token).all()
        assert_that(
            tokens,
            all_of(
                has_items(has_properties(uuid=token_1['uuid'])),
                not_(has_items(has_properties(uuid=token_2['uuid']))),
                not_(has_items(has_properties(uuid=token_3['uuid']))),
            ),
        )

    @fixtures.db.token(expiration=0)
    @fixtures.db.token(expiration=0)
    def test_expired_session_cascade_deletes_token(self, token_1, token_2):
        batch_generator = self._token_dao.purge_expired_tokens_and_sessions(1)

        db_tokens = self.session.query(models.Token).all()
        assert_that(
            db_tokens,
            contains_exactly(
                has_properties(uuid=token_1['uuid']),
                has_properties(uuid=token_2['uuid']),
            ),
        )

        # 1st batch delete
        next(batch_generator)
        db_tokens = self.session.query(models.Token).all()
        assert_that(
            db_tokens,
            contains_exactly(
                has_properties(uuid=token_2['uuid']),
            ),
        )

        # 2nd batch delete
        next(batch_generator)
        db_tokens = self.session.query(models.Token).all()
        assert_that(
            db_tokens,
            empty(),
        )

    @fixtures.db.token(expiration=0)
    @fixtures.db.token(expiration=0)
    @fixtures.db.token(expiration=0)
    def test_expired_tokens_and_sessions_batching(self, token_1, token_2, token_3):
        batch_generator = self._token_dao.get_tokens_and_sessions_about_to_expire(
            0, batch_size=2
        )

        # 1st iteration
        tokens, sessions = next(batch_generator)
        assert_that(
            tokens,
            contains_exactly(
                has_entries(uuid=token_1['uuid']),
                has_entries(uuid=token_2['uuid']),
            ),
        )
        assert_that(
            sessions,
            contains_exactly(
                has_entries(uuid=token_1['session_uuid']),
                has_entries(uuid=token_2['session_uuid']),
            ),
        )

        # 2nd iteration
        tokens, sessions = next(batch_generator)
        assert_that(
            tokens,
            contains_exactly(
                has_entries(
                    uuid=token_3['uuid'],
                )
            ),
        )
        assert_that(
            sessions,
            contains_exactly(
                has_entries(uuid=token_3['session_uuid']),
            ),
        )
