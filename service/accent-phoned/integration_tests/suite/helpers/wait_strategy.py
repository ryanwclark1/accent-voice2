# Copyright 2023 Accent Communications

from accent_test_helpers import until
from accent_test_helpers.wait_strategy import WaitStrategy
from hamcrest import assert_that, only_contains
from requests import ConnectionError, RequestException


class PhonedEverythingUpWaitStrategy(WaitStrategy):
    def wait(self, integration_test):
        def everything_is_up():
            try:
                status = integration_test.get_status_result_by_https()
            except RequestException as e:
                raise AssertionError(f'accent-phoned is not up yet: {e}')
            component_statuses = [
                component['status']
                for component in status.values()
                if 'status' in component
            ]
            assert_that(component_statuses, only_contains('ok'))

        until.assert_(everything_is_up, timeout=10)


class PhonedAPIWaitStrategy(WaitStrategy):
    def wait(self, integration_test):
        def api_is_up():
            try:
                integration_test.get_status_result_by_https()
            except ConnectionError as e:
                raise AssertionError(f'accent-phoned is not up yet: {e}')

        until.assert_(api_is_up, timeout=10)
