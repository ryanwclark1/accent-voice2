# Copyright 2023 Accent Communications

from collections.abc import Generator

import pytest
from accent_test_helpers.asset_launching_test_case import make_asset_fixture

from .helpers.base import BaseAssetLaunchingHelper


@pytest.fixture(scope='session')
def base_asset() -> Generator[BaseAssetLaunchingHelper, None, None]:
    yield from make_asset_fixture(BaseAssetLaunchingHelper)
