# Copyright 2023 Accent Communications

from __future__ import annotations

from collections.abc import Generator

import pytest
from flask import Flask
from flask_restful import Api

from .rest_api import VERSION


@pytest.fixture(name='api')
def api_app() -> Generator[Api, None, None]:
    app = Flask('accent-webhookd-test')
    api = Api(app, prefix=f'/{VERSION}')
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield api
