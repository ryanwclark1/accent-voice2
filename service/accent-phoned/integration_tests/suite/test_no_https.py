# Copyright 2023 Accent Communications

from hamcrest import assert_that, contains_string, equal_to

from .helpers.base import (
    DEFAULT_PROFILE,
    USER_1_UUID,
    VALID_TERM,
    VALID_VENDOR,
    BasePhonedIntegrationTest,
)


class TestHTTPSMissingCertificate(BasePhonedIntegrationTest):
    asset = 'no_ssl_certificate'

    def test_given_inexisting_SSL_certificate_when_phoned_starts_then_phoned_https_stop(
        self,
    ):
        log = self.service_logs('phoned')
        assert_that(log, contains_string("HTTPS server won't start"))

    def test_given_inexisting_SSL_certificate_when_phoned_starts_then_phoned_http_start(
        self,
    ):
        response = self.get_lookup_result(
            vendor=VALID_VENDOR,
            accent_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
        )
        assert_that(response.status_code, equal_to(200))


class TestHTTPSMissingPrivateKey(BasePhonedIntegrationTest):
    asset = 'no_ssl_private_key'

    def test_given_inexisting_SSL_private_key_when_phoned_starts_then_phoned_http_start(
        self,
    ):
        response = self.get_lookup_result(
            vendor=VALID_VENDOR,
            accent_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
        )
        assert_that(response.status_code, equal_to(200))

    def test_given_inexisting_SSL_private_key_when_phoned_starts_then_phoned_https_stop(
        self,
    ):
        log = self.service_logs('phoned')
        assert_that(log, contains_string("HTTPS server won't start"))
