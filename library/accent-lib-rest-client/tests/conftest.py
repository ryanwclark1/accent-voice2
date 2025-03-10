# tests/conftest.py
import httpx
import pytest
from accent_lib_rest_client.client import BaseClient


@pytest.fixture
def mock_httpx_client(mocker):
    """Fixture to mock the httpx.Client."""
    mock_client = mocker.MagicMock(spec=httpx.Client)
    mock_client.__enter__.return_value = mock_client  # For context manager use
    mock_client.__exit__.return_value = None
    return mock_client


@pytest.fixture
def base_client(mock_httpx_client, monkeypatch):
    """Fixture to provide a BaseClient instance with a mocked session."""

    # Use monkeypatch to replace the session method with our mock
    def mock_session(self, *args, **kwargs):
        return mock_httpx_client

    monkeypatch.setattr(BaseClient, "session", mock_session)

    client = BaseClient(host="example.com")
    return client
