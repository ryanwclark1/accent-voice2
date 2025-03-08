# Copyright 2023 Accent Communications

import requests
from accent_test_helpers import until
from accent_test_helpers.wait_strategy import NoWaitStrategy, WaitStrategy
from hamcrest import assert_that, has_entries

__all__ = ['NoWaitStrategy']


class EverythingOkWaitStrategy(WaitStrategy):
    def wait(self, integration_test):
        def is_ready():
            try:
                status = integration_test.plugind.status.get()
            except requests.RequestException:
                status = {}
            assert_that(
                status,
                has_entries(
                    {
                        'master_tenant': has_entries(status='ok'),
                        'rest_api': has_entries(status='ok'),
                    }
                ),
            )

        until.assert_(is_ready, tries=60)
