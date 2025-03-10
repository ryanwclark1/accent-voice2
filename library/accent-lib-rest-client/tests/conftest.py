import pytest
from fastapi.testclient import TestClient

from .fixtures.client import *  # noqa: F403
from .fixtures.commands import *  # noqa: F403


@pytest.fixture
def test_app():
    """Create test FastAPI application."""
    from .server import app
    return app

@pytest.fixture
def test_client(test_app):
    """Create FastAPI test client."""
    return TestClient(test_app)
