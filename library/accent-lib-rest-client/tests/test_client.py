# tests/test_client.py
import logging  # Import the logging module
import pytest
import httpx
from uuid import UUID, uuid4
from accent_lib_rest_client.client import BaseClient
from accent_lib_rest_client.models import ClientConfig


def test_client_initialization(mock_httpx_client):
    """Test basic client initialization and configuration."""
    client = BaseClient(
        host="example.com", port=8080, https=False, prefix="/api", version="v1"
    )
    assert client._host == "example.com"
    assert client._port == 8080
    assert client._https is False
    assert client._prefix == "/api"
    assert client._version == "/v1"  # Expect leading slash
    assert client.config.host == "example.com"  # Check Pydantic model
    assert isinstance(client.config, ClientConfig)
    assert client._url_config.build_base_url() == "http://example.com:8080/api/v1"


def test_url_construction(base_client):
    """Test URL construction with various fragments."""
    assert base_client.url("users", "123") == "http://example.com:443/users/123"
    assert (
        base_client.url("users", "123", "posts")
        == "http://example.com:443/users/123/posts"
    )
    assert base_client.url() == "http://example.com:443/"


def test_tenant_uuid_handling(base_client):
    """Test setting and getting the tenant UUID."""
    test_uuid = uuid4()
    base_client.tenant_uuid = test_uuid
    assert base_client.tenant_uuid == test_uuid
    base_client.tenant_uuid = str(test_uuid)  # Test string conversion
    assert base_client.tenant_uuid == test_uuid
    assert base_client._tenant_config.tenant_uuid == test_uuid


def test_set_token(base_client):
    """Test setting the authentication token."""
    test_token = "test-token-123"
    base_client.set_token(test_token)
    assert base_client._token == test_token
    assert base_client._token_config.token == test_token


def test_session_creation(base_client, mock_httpx_client):
    """Test session creation and header configuration."""

    with base_client.session() as session:
        assert session == mock_httpx_client  # Check it's our mocked client
        mock_httpx_client.headers.update.assert_any_call(
            {"Connection": "close"}
        )  # Check for base header
        mock_httpx_client.headers.update.assert_any_call({"User-agent": ""})

        # Test with tenant and token
        test_uuid = uuid4()
        base_client.tenant_uuid = test_uuid
        base_client.set_token("test-token")

        session = base_client.session()
        mock_httpx_client.headers.update.assert_any_call({"X-Auth-Token": "test-token"})
        mock_httpx_client.headers.update.assert_any_call(
            {"Accent-Tenant": str(test_uuid)}
        )


def test_server_reachability_success(base_client, mock_httpx_client):
    """Test successful server reachability check."""
    mock_httpx_client.head.return_value.status_code = 200  # Mock a successful response
    mock_httpx_client.head.return_value.raise_for_status.return_value = (
        None  # Mock no http error
    )
    assert base_client.is_server_reachable() is True
    mock_httpx_client.head.assert_called_once_with("http://example.com:443/")


def test_server_reachability_http_error(base_client, mock_httpx_client):
    """Test server reachability with an HTTP error (but server is reachable)."""
    mock_httpx_client.head.return_value.status_code = 500  # Return an error code
    mock_httpx_client.head.side_effect = httpx.HTTPStatusError(
        "Mock Error",
        request=httpx.Request("head", "http://example.com"),
        response=httpx.Response(
            500, request=httpx.Request("head", "http://example.com")
        ),
    )

    assert (
        base_client.is_server_reachable() is True
    )  # HTTP error doesn't mean unreachable
    mock_httpx_client.head.assert_called_once_with("http://example.com:443/")


def test_server_reachability_connection_error(base_client, mock_httpx_client):
    """Test server reachability with a connection error."""
    mock_httpx_client.head.side_effect = httpx.ConnectError("Mock Connection Error")

    assert base_client.is_server_reachable() is False
    mock_httpx_client.head.assert_called_once_with("http://example.com:443/")


def test_client_extra_kwargs_warning(caplog):
    """Test that extra kwargs passed to the client constructor log a warning."""
    with caplog.at_level(logging.DEBUG):
        _ = BaseClient(host="example.com", extra_arg="some_value")
    assert "received unexpected arguments" in caplog.text
    assert "extra_arg" in caplog.text
