# Copyright 2023 Accent Communications

import requests
from accent_test_helpers import until
from accent_test_helpers.wait_strategy import WaitStrategy
from hamcrest import assert_that, has_entries


class RestAPIOkWaitStrategy(WaitStrategy):
    def wait(self, integration_test):
        def is_ready():
            try:
                status = integration_test.confd.status.get().item
            except requests.RequestException:
                status = {}
            assert_that(
                status,
                has_entries(
                    {
                        'rest_api': has_entries(status='ok'),
                    }
                ),
            )

        until.assert_(is_ready, tries=60)


class EverythingOkWaitStrategy(WaitStrategy):
    def wait(self, integration_test):
        def is_ready():
            try:
                status = integration_test.confd.status.get().item
            except requests.RequestException:
                status = {}
            assert_that(
                status,
                has_entries(
                    {
                        'rest_api': has_entries(status='ok'),
                        'bus_consumer': has_entries(status='ok'),
                        'master_tenant': has_entries(status='ok'),
                        'service_token': has_entries(status='ok'),
                    }
                ),
            )

        until.assert_(is_ready, tries=60)
