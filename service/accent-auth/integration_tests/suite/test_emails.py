# Copyright 2023 Accent Communications

from accent_test_helpers.hamcrest.uuid_ import uuid_
from hamcrest import assert_that, contains_inanyorder, empty, has_entries

from .helpers import base, fixtures
from .helpers.base import assert_http_error
from .helpers.constants import UNKNOWN_UUID

ONE = {'address': 'one@example.com', 'main': True, 'confirmed': True}
TWO = {'address': 'two@example.com', 'main': False, 'confirmed': False}
THREE = {'address': 'three@example.com', 'main': False, 'confirmed': True}


@base.use_asset('base')
class TestEmails(base.APIIntegrationTest):
    @fixtures.http.user(username='foobar')
    def test_email_updates_as_admin(self, foobar):
        assert_http_error(404, self.client.admin.update_user_emails, UNKNOWN_UUID, [])
        assert_http_error(
            400, self.client.users.update_emails, foobar['uuid'], [ONE, ONE]
        )

        result = self.client.admin.update_user_emails(foobar['uuid'], [ONE, TWO])
        assert_that(
            result,
            contains_inanyorder(
                has_entries(uuid=uuid_(), **ONE), has_entries(uuid=uuid_(), **TWO)
            ),
        )

        one_uuid = [
            entry['uuid'] for entry in result if entry['address'] == 'one@example.com'
        ][0]
        result = self.client.admin.update_user_emails(foobar['uuid'], [ONE, THREE])
        assert_that(
            result,
            contains_inanyorder(
                has_entries(uuid=one_uuid, **ONE), has_entries(uuid=uuid_(), **THREE)
            ),
        )

    @fixtures.http.user(username='foobar', email_address='one@example.com')
    def test_email_updates_as_user(self, foobar):
        assert_http_error(404, self.client.users.update_emails, UNKNOWN_UUID, [])
        assert_http_error(
            400, self.client.users.update_emails, foobar['uuid'], [ONE, ONE]
        )

        email_uuid = foobar['emails'][0]['uuid']
        result = self.client.users.update_emails(foobar['uuid'], [ONE, THREE])
        assert_that(
            result,
            contains_inanyorder(
                has_entries(uuid=email_uuid, **ONE),
                has_entries(
                    uuid=uuid_(),
                    address=THREE['address'],
                    main=THREE['main'],
                    confirmed=False,
                ),
                # Confirmed is ignored when modifying as a user
            ),
        )

        result = self.client.users.update_emails(foobar['uuid'], [])
        assert_that(result, empty())

    @fixtures.http.user(username='foo', email_address='foo@example.com')
    @fixtures.http.user(username='bar', email_address='bar@example.com')
    def test_duplicate_email(self, foo, bar):
        duplicated_emails = [
            {'address': 'bar@example.com', 'main': True, 'confirmed': True},
            {'address': 'bAr@example.com', 'main': True, 'confirmed': True},
        ]
        for duplicate in duplicated_emails:
            assert_http_error(
                409, self.client.users.update_emails, foo['uuid'], [duplicate]
            )

    @fixtures.http.user()
    @fixtures.http.user(username='u2@example.com')
    @fixtures.http.user(email_address='u3@example.com')
    def test_email_same_login(self, u1, u2, u3):
        uuid = u1['uuid']

        email = {'address': 'u2@example.com', 'main': True, 'confirmed': True}
        assert_http_error(409, self.client.users.update_emails, uuid, [email])

        email = {'address': 'u2@example.com', 'main': True, 'confirmed': False}
        assert_http_error(409, self.client.users.update_emails, uuid, [email])

        email = {'address': 'U2@exAmple.com', 'main': True, 'confirmed': True}
        assert_http_error(409, self.client.users.update_emails, uuid, [email])

        email = {'address': 'U2@exAmple.com', 'main': True, 'confirmed': False}
        assert_http_error(409, self.client.users.update_emails, uuid, [email])

        email = {'address': 'u3@example.com', 'main': True, 'confirmed': True}
        assert_http_error(409, self.client.users.update_emails, uuid, [email])

        email = {'address': 'u3@example.com', 'main': True, 'confirmed': False}
        assert_http_error(409, self.client.users.update_emails, uuid, [email])

        email = {'address': 'U3@exAmple.com', 'main': True, 'confirmed': True}
        assert_http_error(409, self.client.users.update_emails, uuid, [email])

        email = {'address': 'U3@exAmple.com', 'main': True, 'confirmed': False}
        assert_http_error(409, self.client.users.update_emails, uuid, [email])
