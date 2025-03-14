# Copyright 2023 Accent Communications

from unittest import TestCase

from accent_test_helpers.hamcrest.raises import raises
from hamcrest import assert_that, calling, has_key, has_properties, not_
from marshmallow.exceptions import ValidationError

from ..schemas import TokenRequestSchema


class TestTokenRequestSchema(TestCase):
    def setUp(self):
        self.schema = TokenRequestSchema()

    def test_invalid_expiration(self):
        invalid_values = [None, True, False, 'foobar', 0]

        for value in invalid_values:
            body = {'expiration': value}
            assert_that(
                calling(self.schema.load).with_args(body),
                raises(ValidationError).matching(
                    has_properties(messages=has_key('expiration'))
                ),
            )

    def test_minimal_body(self):
        body = {}
        assert_that(calling(self.schema.load).with_args(body), not_(raises(Exception)))

    def test_that_acces_type_offline_requires_a_client_id(self):
        body = {'access_type': 'offline'}

        assert_that(
            calling(self.schema.load).with_args(body),
            raises(ValidationError).matching(has_properties(field_name='_schema')),
        )

    def test_that_the_access_type_is_online_when_using_a_refresh_token(self):
        body = {'refresh_token': 'foobar', 'client_id': 'x'}

        assert_that(calling(self.schema.load).with_args(body), not_(raises(Exception)))

        assert_that(
            calling(self.schema.load).with_args({'access_type': 'online', **body}),
            not_(raises(Exception)),
        )

        assert_that(
            calling(self.schema.load).with_args({'access_type': 'offline', **body}),
            raises(ValidationError).matching(has_properties(field_name='_schema')),
        )

    def test_that_a_refresh_token_requires_a_client_id(self):
        body = {'refresh_token': 'the-token'}

        assert_that(
            calling(self.schema.load).with_args({'client_id': 'x', **body}),
            not_(raises(Exception)),
        )

        assert_that(
            calling(self.schema.load).with_args(body),
            raises(ValidationError).matching(has_properties(field_name='_schema')),
        )

    def test_that_using_both_tenant_id_and_domain_name_raises_400(self):
        body = {'tenant_id': 'x', 'domain_name': 'accentvoice.io'}

        assert_that(
            calling(self.schema.load).with_args(body),
            raises(ValidationError).matching(has_properties(field_name='_schema')),
        )
