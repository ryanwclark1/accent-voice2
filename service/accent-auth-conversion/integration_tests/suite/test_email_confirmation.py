# Copyright 2023 Accent Communications

import requests
from hamcrest import (
    assert_that,
    contains_exactly,
    equal_to,
    has_entries,
    has_properties,
    starts_with,
)

from .helpers import base, fixtures
from .helpers.base import assert_http_error, assert_no_error
from .helpers.constants import UNKNOWN_UUID


@base.use_asset('base')
class TestEmailConfirmation(base.APIIntegrationTest):
    @fixtures.http.user_register(email_address='foobar@example.com')
    def test_email_confirmation(self, user):
        email_uuid = user['emails'][0]['uuid']

        assert_http_error(404, self.client.emails.confirm, UNKNOWN_UUID)
        assert_no_error(self.client.emails.confirm, email_uuid)

        updated_user = self.client.users.get(user['uuid'])
        assert_that(
            updated_user,
            has_entries(
                emails=contains_exactly(
                    has_entries(address='foobar@example.com', confirmed=True)
                )
            ),
        )

    @fixtures.http.user_register(email_address='foobar@example.com')
    def test_email_confirmation_get(self, user):
        email_uuid = user['emails'][0]['uuid']
        url = f'http://127.0.0.1:{self.auth_port()}/0.1/emails/{email_uuid}/confirm'
        token = self.client._token_id
        response = requests.get(url, params={'token': token})
        assert_that(response.status_code, equal_to(200))

        updated_user = self.client.users.get(user['uuid'])
        assert_that(
            updated_user,
            has_entries(
                emails=contains_exactly(
                    has_entries(address='foobar@example.com', confirmed=True)
                )
            ),
        )

    @fixtures.http.user_register(email_address='foobar@example.com')
    def test_sending_a_new_confirmation_mail(self, user):
        email_uuid = user['emails'][0]['uuid']

        self.client.users.request_confirmation_email(user['uuid'], email_uuid)

        expected_url = (
            f'https://127.0.0.1:{self.auth_port()}/0.1/emails/.*/confirm\\?token=.*'
        )
        self.assert_last_email(
            from_name='confirmation_from_name_sentinel',
            from_address='confirmation_from_address_sentinel@example.com',
            to_name=user['username'],
            to_address='foobar@example.com',
            body_contains=expected_url,
        )

        url = self.get_last_email_url()
        url = url.replace('https://', 'http://')
        result = requests.get(url)
        assert_that(
            result,
            has_properties(
                status_code=200,
                headers=has_entries(
                    'Content-Type', starts_with('text/x-test; charset=')
                ),
                text='Custom template',
            ),
        )

        updated_user = self.client.users.get(user['uuid'])
        assert_that(
            updated_user,
            has_entries(
                emails=contains_exactly(
                    has_entries(address='foobar@example.com', confirmed=True)
                )
            ),
        )

        assert_http_error(
            409, self.client.users.request_confirmation_email, user['uuid'], email_uuid
        )
        assert_http_error(
            404, self.client.users.request_confirmation_email, UNKNOWN_UUID, email_uuid
        )
        assert_http_error(
            404,
            self.client.users.request_confirmation_email,
            user['uuid'],
            UNKNOWN_UUID,
        )
