# Copyright 2023 Accent Communications

from accent_provd_client.exceptions import ProvdError
from accent_test_helpers.hamcrest.raises import raises
from hamcrest import assert_that, calling, has_properties

from .helpers.base import BaseIntegrationTest


class TestAuthentication(BaseIntegrationTest):
    asset = 'base'

    def test_no_token(self) -> None:
        client = self.make_provd('')

        assert_that(
            calling(client.status.get),
            raises(ProvdError).matching(has_properties('status_code', 401)),
        )

    def test_invalid_token(self) -> None:
        client = self.make_provd('invalid')

        assert_that(
            calling(client.status.get),
            raises(ProvdError).matching(has_properties('status_code', 401)),
        )
