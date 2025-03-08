import httpx
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def mock_client(mocker):
    """Create a mock client for testing."""
    client = mocker.Mock()
    client.timeout = mocker.sentinel.timeout
    client.tenant_uuid = None
    client._token = None
    client.url = mocker.Mock(return_value="http://test.com/api")
    return client

@pytest.fixture
def mock_session(mocker, mock_client):
    """Create a mock session for testing."""
    session = mocker.Mock(spec=httpx.Client)
    session.headers = {}
    mock_client.session.return_value = session
    return session

@pytest.fixture
def mock_response(mocker):
    """Create a mock HTTP response."""
    response = mocker.Mock(spec=httpx.Response)
    response.status_code = 200
    response.json.return_value = {"status": "success"}
    return response

@pytest.fixture
def error_response(mocker):
    """Create a mock error response."""
    response = mocker.Mock(spec=httpx.Response)
    response.status_code = 404
    response.text = "Not Found"
    return response