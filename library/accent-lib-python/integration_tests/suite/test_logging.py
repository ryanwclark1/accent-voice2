# Copyright 2023 Accent Communications

import os

from accent_test_helpers.asset_launching_test_case import AssetLaunchingTestCase
from hamcrest import assert_that, contains_string

ASSET_ROOT = os.path.join(os.path.dirname(__file__), "..", "assets")


class _BaseTest(AssetLaunchingTestCase):
    assets_root = ASSET_ROOT
    service = "thread-exception"
    asset = "thread-exception"

    def test_thread_exception_is_logged(self) -> None:
        logs = self.service_logs("thread-exception")

        assert_that(logs, contains_string("exception is logged"))
