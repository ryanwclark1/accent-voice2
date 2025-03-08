# Copyright 2023 Accent Communications

import requests
from accent_test_helpers import until
from accent_test_helpers.wait_strategy import NoWaitStrategy, WaitStrategy
from hamcrest import assert_that, has_entries

__all__ = ['NoWaitStrategy']


class RestApiOkWaitStrategy(WaitStrategy):
    def wait(self, dird):
        def is_ready():
            try:
                status = dird.status.get()
            except requests.RequestException:
                status = {}
            assert_that(
                status,
                has_entries(
                    {
                        'rest_api': has_entries(status='ok'),
                        'master_tenant': has_entries(status='ok'),
                    }
                ),
            )

        until.assert_(is_ready, tries=60)


class EverythingOkWaitStrategy(WaitStrategy):
    def wait(self, dird):
        def is_ready():
            try:
                status = dird.status.get()
            except requests.RequestException:
                status = {}
            assert_that(
                status,
                has_entries(
                    {
                        'rest_api': has_entries(status='ok'),
                        'bus_consumer': has_entries(status='ok'),
                        'master_tenant': has_entries(status='ok'),
                    }
                ),
            )

        until.assert_(is_ready, tries=60)
