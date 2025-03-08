# Copyright 2023 Accent Communications

from typing import Any

import requests
from accent_test_helpers import until
from accent_test_helpers.wait_strategy import WaitStrategy
from hamcrest import assert_that, has_entries


class EverythingOkWaitStrategy(WaitStrategy):
    def wait(self, integration_test: Any) -> None:
        def is_ready() -> None:
            try:
                status = integration_test.amid.status()
            except requests.RequestException:
                status = {}
            assert_that(
                status,
                has_entries(
                    {
                        'rest_api': has_entries(status='ok'),
                        'ami_socket': has_entries(status='ok'),
                        'service_token': has_entries(status='ok'),
                    }
                ),
            )

        until.assert_(is_ready, tries=60)
