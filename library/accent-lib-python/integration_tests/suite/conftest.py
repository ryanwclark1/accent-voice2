# Copyright 2023 Accent Communications

from collections.abc import Iterator

import pytest
from accent_test_helpers.asset_launching_test_case import NoSuchService
from pytest import FixtureRequest


@pytest.fixture(autouse=True, scope="function")
def mark_logs(request: FixtureRequest) -> Iterator[None]:
    test_name = f"{request.cls.__name__}.{request.function.__name__}"
    try:
        request.cls.mark_logs_test_start(test_name)
    except NoSuchService:
        pass

    yield

    try:
        request.cls.mark_logs_test_end(test_name)
    except NoSuchService:
        pass
