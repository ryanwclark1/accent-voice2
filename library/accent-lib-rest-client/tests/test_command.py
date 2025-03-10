# tests/test_command.py
import pytest
import httpx
from pydantic import BaseModel, ValidationError
from pytest_mock import MockerFixture
from accent_lib_rest_client.command import HTTPCommand, RESTCommand
from accent_lib_rest_client.exceptions import HTTPError, ResponseValidationError

# --- Test HTTPCommand ---


class MockClient:  # Minimal mock client for HTTPCommand tests
    def session(self):
        return httpx.Client()


@pytest.fixture
def http_command():
    client = MockClient()
    return HTTPCommand(client)


def test_http_command_session(http_command):
    """Test that session property returns an httpx.Client instance."""
    session = http_command.session
    assert isinstance(session, httpx.Client)


def test_validate_response_success(http_command, mocker: MockerFixture):
    """Test successful response validation."""
    mock_response = mocker.MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}
    mock_response.raise_for_status.return_value = None

    data = http_command.validate_response(mock_response)
    assert data == {"key": "value"}
    mock_response.json.assert_called_once()


def test_validate_response_with_model_success(http_command, mocker: MockerFixture):
    """Test response validation with a Pydantic model."""

    class TestModel(BaseModel):
        key: str

    mock_response = mocker.MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}
    mock_response.raise_for_status.return_value = None

    validated_data = http_command.validate_response(mock_response, TestModel)
    assert isinstance(validated_data, TestModel)
    assert validated_data.key == "value"
    mock_response.json.assert_called_once()


def test_validate_response_with_model_validation_error(
    http_command, mocker: MockerFixture
):
    """Test response validation with a Pydantic model and validation error."""

    class TestModel(BaseModel):
        key: int  # Expecting an integer

    mock_response = mocker.MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "not an integer"}  # Invalid data
    mock_response.raise_for_status.return_value = None

    with pytest.raises(ResponseValidationError):
        http_command.validate_response(mock_response, TestModel)
    mock_response.json.assert_called_once()


def test_validate_response_http_error(http_command, mocker: MockerFixture):
    """Test response validation with an HTTP error."""
    mock_response = mocker.MagicMock(spec=httpx.Response)
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Not Found", request=mocker.Mock(), response=mock_response
    )

    with pytest.raises(HTTPError) as exc_info:
        http_command.validate_response(mock_response)

    assert exc_info.value.response == mock_response  # Check response is stored


# --- Test RESTCommand ---


class MockRESTClient:
    """Mock client for testing RESTCommand, providing url and timeout."""

    def __init__(self, mock_session):
        self.mock_session = mock_session

    def url(self, *fragments):
        return "/".join(fragments)  # Simple URL joining

    @property  # Make session a property
    def session(self):
        return self.mock_session

    timeout = 10


@pytest.fixture
def rest_command(mocker: MockerFixture):
    class TestRESTCommand(RESTCommand):
        resource = "test_resource"  # Must define 'resource'

    mock_session = mocker.MagicMock(spec=httpx.Client)
    # Pass the mock session to the MockRESTClient
    client = MockRESTClient(mock_session=mock_session)
    return TestRESTCommand(client)


def test_rest_command_initialization(rest_command):
    """Test RESTCommand initialization and base_url."""
    assert rest_command.base_url == "test_resource"
    assert rest_command.timeout == 10


def test_rest_command_get_headers(rest_command):
    """Test header generation, including tenant ID."""
    headers = rest_command._get_headers()
    assert headers == {"Accept": "application/json"}

    headers = rest_command._get_headers(tenant_uuid="test-tenant")
    assert headers == {"Accept": "application/json", "Accent-Tenant": "test-tenant"}

    headers = rest_command._get_headers(tenant_uuid="test-tenant", Custom="Value")
    assert headers == {
        "Accept": "application/json",
        "Accent-Tenant": "test-tenant",
        "Custom": "Value",
    }


@pytest.mark.parametrize("method", ["get", "post", "put", "delete"])
def test_rest_command_http_methods(rest_command, method, mocker: MockerFixture):
    """Test the get, post, put, and delete methods of RESTCommand."""

    mock_response = mocker.MagicMock(spec=httpx.Response)
    mock_response.json.return_value = {"result": "success"}  # Mock the json method
    rest_command._client.mock_session.request.return_value = mock_response

    # Get the correct method from the rest_command instance
    command_method = getattr(rest_command, method)

    # Call the method.  Pass json data for post/put, nothing for get/delete
    if method in ("post", "put"):
        result = command_method("path", json={"data": "test"})
    else:
        result = command_method("path")

    assert result == {"result": "success"}

    rest_command._client.mock_session.request.assert_called_once_with(
        method.upper(),
        "test_resource/path",
        headers={"Accept": "application/json"},
        json={"data": "test"} if method in ("post", "put") else None,  # Check json data
    )
