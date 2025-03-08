# Copyright 2023 Accent Communications

import requests
from accent_test_helpers import until
from accent_test_helpers.wait_strategy import ComponentsWaitStrategy, WaitStrategy
from hamcrest import assert_that, only_contains


class CallLogdComponentsWaitStrategy(ComponentsWaitStrategy):
    def get_status(self, integration_test):
        return integration_test.call_logd.status.get()


class CallLogdEverythingUpWaitStrategy(WaitStrategy):
    def wait(self, integration_test):
        def everything_is_up():
            try:
                status = integration_test.call_logd.status.get()
            except requests.RequestException:
                status = {}

            component_statuses = [
                component['status']
                for component in status.values()
                if 'status' in component
            ]
            assert_that(component_statuses, only_contains('ok'))

        until.assert_(everything_is_up, timeout=10)
