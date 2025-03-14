# Copyright 2023 Accent Communications

import unittest

from accent_test_helpers.hamcrest.raises import raises
from hamcrest import (
    assert_that,
    calling,
    contains_exactly,
    equal_to,
    has_entries,
    has_property,
    not_,
)
from marshmallow import ValidationError

from ..schemas import PasswordResetQueryParameters


class TestSchema(unittest.TestCase):
    def setUp(self):
        self.password_query_parameters_schema = PasswordResetQueryParameters()

    def test_the_email_field(self):
        email = 'foobar@example.com'
        query_string = {'email': email}

        result = self.password_query_parameters_schema.load(query_string)

        assert_that(result, has_entries(email_address=email))

    def test_that_username_and_email_and_login_are_mutually_exclusive(self):
        queries = [
            {'email': 'foo@bar.com', 'username': 'foobar', 'login': 'foo'},
            {'email': 'foo@bar.com', 'username': None, 'login': 'foo'},
            {'email': 'foo@bar.com', 'username': 'foobar', 'login': None},
            {'email': None, 'username': 'foobar', 'login': 'foo'},
        ]

        for query in queries:
            assert_that(
                calling(self.password_query_parameters_schema.load).with_args(query),
                raises(
                    ValidationError,
                    has_property(
                        "messages",
                        has_entries(
                            _schema=contains_exactly(
                                '"username" or "email" or "login" should be used'
                            )
                        ),
                    ),
                ),
            )

    def test_username_only(self):
        query_string = {'username': 'foobar'}

        result = self.password_query_parameters_schema.load(query_string)

        assert_that(
            result,
            has_entries(
                username='foobar',
                email_address=None,
                login=None,
            ),
        )

    def test_email_only(self):
        query_string = {'email': 'foobar@example.com'}

        result = self.password_query_parameters_schema.load(query_string)

        assert_that(
            result,
            has_entries(
                username=None,
                email_address='foobar@example.com',
                login=None,
            ),
        )

    def test_login_only(self):
        query_string = {'login': 'foobar@example.com'}

        result = self.password_query_parameters_schema.load(query_string)

        assert_that(
            result,
            has_entries(
                username=None,
                email_address=None,
                login='foobar@example.com',
            ),
        )

    def test_invalid_field(self):
        query_string = {'username': 300 * 'a'}
        assert_that(
            calling(self.password_query_parameters_schema.load).with_args(query_string),
            raises(ValidationError, has_property("messages", not_(equal_to(None)))),
        )

        query_string = {'email': 'patate'}
        assert_that(
            calling(self.password_query_parameters_schema.load).with_args(query_string),
            raises(ValidationError, has_property("messages", not_(equal_to(None)))),
        )
