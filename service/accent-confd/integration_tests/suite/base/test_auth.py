# Copyright 2023 Accent Communications

from accent_test_helpers import until

from ..helpers.wait_strategy import RestAPIOkWaitStrategy
from . import BaseIntegrationTest, confd, confd_with_config


def test_restrict_when_service_token_not_initialized():
    def _returns_503():
        response = confd.extensions.features.get()
        response.assert_status(503)

    config = {'auth': {'username': 'invalid-service'}}
    with confd_with_config(config):
        RestAPIOkWaitStrategy().wait(BaseIntegrationTest)
        until.assert_(_returns_503, tries=10)
