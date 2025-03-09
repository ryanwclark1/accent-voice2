# tests/test_models.py
import pytest
from pydantic import ValidationError
from accent_lib_rest_client.models import (
    URLConfig,
    RequestParameters,
    ErrorResponse,
    ClientConfig,
    TenantConfig,
    TokenConfig,
)
from datetime import datetime
from uuid import uuid4


def test_url_config():
    """Test URLConfig model."""
    config = URLConfig(
        scheme="https", host="example.com", port=8080, prefix="/api", version="v1"
    )
    assert config.scheme == "https"
    assert config.host == "example.com"
    assert config.port == 8080
    assert config.prefix == "/api"
    assert config.version == "/v1"
    assert config.build_base_url() == "https://example.com:8080/api/v1"
    assert (
        config.build_url("users", "123") == "https://example.com:8080/api/v1/users/123"
    )

    with pytest.raises(ValidationError):
        URLConfig(scheme="invalid", host="example.com")  # Invalid scheme
    with pytest.raises(ValidationError):
        URLConfig(scheme="http", host="invalid-url")  # Invalid host
    with pytest.raises(ValidationError):
        URLConfig(scheme="http", host="example.com", port=-1)  # Invalid Port


def test_request_parameters():
    """Test RequestParameters model."""
    params = RequestParameters(timeout=30, verify_ssl=False)
    assert params.timeout == 30
    assert params.verify_ssl is False
    assert params.tenant_uuid is None

    test_uuid = uuid4()
    params = RequestParameters(tenant_uuid=test_uuid)
    assert params.tenant_uuid == test_uuid


def test_error_response():
    """Test ErrorResponse model."""
    timestamp = datetime.now()
    error = ErrorResponse(
        message="Test Error",
        error_id="err_123",
        details="Some details",
        timestamp=timestamp,
    )
    assert error.message == "Test Error"
    assert error.error_id == "err_123"
    assert error.details == "Some details"
    assert error.timestamp == timestamp


def test_client_config():
    """Test ClientConfig model."""
    test_uuid = uuid4()
    config = ClientConfig(
        host="example.net",
        https=False,
        port=8000,
        tenant_uuid=str(test_uuid),
        prefix="api",
        version="v2",
        timeout=15,
        token="test-token",
        user_agent="Test Agent",
        verify_certificate=False,
    )
    assert config.host == "example.net"
    assert config.https is False
    assert config.port == 8000
    assert config.prefix == "/api"  # Leading slash added
    assert config.version == "/v2"  # Leading slash added
    assert config.tenant_uuid == test_uuid
    assert config.timeout == 15
    assert config.token == "test-token"
    assert config.user_agent == "Test Agent"
    assert config.verify_certificate is False
    assert config.build_base_url() == "http://example.net:8000/api/v2"

    with pytest.raises(ValidationError):
        ClientConfig(host="example.com", port=70000)  # Check high port range
    with pytest.raises(ValidationError):
        ClientConfig(host="example.com", timeout=-1)  # Check timeout


def test_tenant_config():
    test_uuid = uuid4()
    tenant_config = TenantConfig(tenant_uuid=str(test_uuid))
    assert tenant_config.tenant_uuid == test_uuid
    assert tenant_config.tenant_enabled == True  # Check default

    tenant_config = TenantConfig(tenant_uuid=test_uuid, tenant_enabled=False)
    assert tenant_config.tenant_enabled == False


def test_token_config():
    timestamp = datetime.now()
    token_config = TokenConfig(
        token="test-token", token_type="JWT", expires_at=timestamp
    )
    assert token_config.token == "test-token"
    assert token_config.token_type == "JWT"
    assert token_config.expires_at == timestamp

    token_config = TokenConfig(token="test-token")  # Check defaults
    assert token_config.token_type == "Bearer"
    assert token_config.expires_at is None
