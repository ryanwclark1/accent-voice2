# Copyright 2023 Accent Communications

import requests
from accent_test_helpers import until
from hamcrest import assert_that, has_entries


class WaitStrategy:
    def wait(self, chatd):
        raise NotImplementedError()


class NoWaitStrategy(WaitStrategy):
    def wait(self, chatd):
        pass


class EverythingOkWaitStrategy(WaitStrategy):
    def wait(self, integration_test):
        def is_ready():
            try:
                status = integration_test.chatd.status.get()
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


class RestApiOkWaitStrategy(WaitStrategy):
    def wait(self, integration_test):
        def is_ready():
            try:
                status = integration_test.chatd.status.get()
            except requests.RequestException:
                status = {}
            assert_that(status, has_entries({'rest_api': has_entries(status='ok')}))

        until.assert_(is_ready, tries=60)


class PresenceInitOkWaitStrategy(WaitStrategy):
    def wait(self, integration_test):
        def is_ready():
            try:
                status = integration_test.chatd.status.get()
            except requests.RequestException:
                status = {}
            assert_that(
                status,
                has_entries(
                    {
                        'presence_initialization': has_entries(status='ok'),
                        'rest_api': has_entries(status='ok'),
                        'bus_consumer': has_entries(status='ok'),
                    }
                ),
            )

        until.assert_(is_ready, tries=60)
