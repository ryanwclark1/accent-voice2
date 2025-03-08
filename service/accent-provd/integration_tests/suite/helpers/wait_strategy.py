# Copyright 2023 Accent Communications

import requests
from accent_test_helpers import until
from accent_test_helpers.wait_strategy import WaitStrategy as DefaultWaitStrategy
from hamcrest import assert_that, has_entries


class WaitStrategy:
    def wait(self, setupd):
        raise NotImplementedError()


class NoWaitStrategy(WaitStrategy):
    def wait(self, provd):
        pass


class EverythingOkWaitStrategy(DefaultWaitStrategy):
    def wait(self, integration_test):
        def is_ready():
            try:
                status = integration_test._client.status.get()
            except requests.RequestException:
                status = {}
            assert_that(
                status,
                has_entries(
                    {
                        'rest_api': 'ok',
                        'bus_consumer': has_entries(status='ok'),
                    }
                ),
            )

        until.assert_(is_ready, tries=60)
