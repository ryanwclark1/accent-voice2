# Copyright 2023 Accent Communications

import requests
from accent_test_helpers import until
from hamcrest import (
    assert_that,
    has_entries,
    has_entry,
)


class WaitStrategy:
    def wait(self, setupd):
        raise NotImplementedError()


class NoWaitStrategy(WaitStrategy):
    def wait(self, setupd):
        pass


class SetupdEverythingOkWaitStrategy(WaitStrategy):
    def wait(self, setupd):
        def setupd_is_ready():
            try:
                status = setupd.status.get()
            except requests.RequestException:
                status = {}
            assert_that(
                status,
                has_entries(
                    {
                        'rest_api': has_entry('status', 'ok'),
                        'master_tenant': has_entry('status', 'ok'),
                    }
                ),
            )

        until.assert_(setupd_is_ready, tries=60)
