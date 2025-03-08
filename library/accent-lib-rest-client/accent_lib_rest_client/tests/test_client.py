# Copyright 2023 Accent Communications

from __future__ import annotations

import asyncio
import time
from uuid import UUID

import httpx
import pytest

from accent_lib_rest_client.client import BaseClient
from accent_lib_rest_client.example_cmd import ExampleCommand
from accent_lib_rest_client.exceptions import HTTPError


class TestClient(BaseClient):
    namespace = 'test_rest_client.commands'
    example: ExampleCommand

    def __init__(
        self,
        host='localhost',
        port=1234,
        version='1.1',
        username=None,
        password=None,
        https=False,
        verify_certificate=False,
        **kwargs,
    ):
        super().__init__(
            host=host,
            port=port,
            version=version,
            https=https,
            verify_certificate=verify_certificate,
            **kwargs,
        )
        self.username = username
        self.password = password

class MockSessionClient(BaseClient):
    namespace = 'some-namespace'

    def __init__(self, session: httpx.Client) -> None:
        super().__init__('localhost', 1234)
        self._session = session

    def session(self) -> httpx.Client:
        return self._session

@pytest.fixture
def client():
    return TestClient()

def test_url_construction(client):
    """Test URL construction with various parameters."""
    assert client.url().startswith('http://')

    client = TestClient(https=True)
    assert client.url().startswith('https://')

    client = TestClient(host='example.com', port=8080, version='v2')
    assert client.url() == 'http://example.com:8080/v2'

def test_prefix_handling():
    """Test prefix handling in URLs."""
    client = TestClient(prefix='/api')
    assert '/api/' in client.url()

    client = TestClient(prefix='api')  # Missing leading slash
    assert '/api/' in client.url()

@pytest.mark.parametrize('token_value', [
    'test-token',
    'bearer-token-123',
])
def test_token_handling(token_value):
    """Test token handling in headers."""
    client = TestClient(token=token_value)
    with client.session() as session:
        assert session.headers.get('X-Auth-Token') == token_value

def test_tenant_uuid_handling():
    """Test tenant UUID handling."""
    test_uuid = "550e8400-e29b-41d4-a716-446655440000"
    client = TestClient(tenant_uuid=test_uuid)
    assert isinstance(client.tenant_uuid, UUID)

    # Test string UUID conversion
    client.tenant_uuid = test_uuid
    assert isinstance(client.tenant_uuid, UUID)

@pytest.mark.asyncio
async def test_server_reachability():
    """Test server reachability check."""
    client = TestClient()

    # Mock successful response
    with patch('httpx.Client.head') as mock_head:
        mock_head.return_value.status_code = 200
        assert client.is_server_reachable() is True

    # Mock connection error
    with patch('httpx.Client.head') as mock_head:
        mock_head.side_effect = httpx.RequestError("Connection failed")
        assert client.is_server_reachable() is False

def test_extra_kwargs_are_logged(caplog):
    """Test that extra kwargs are logged."""
    TestClient(extra_param=True)
    assert "received unexpected arguments" in caplog.text
    assert "extra_param" in caplog.text

def test_timeout_handling():
    """Test timeout behavior."""
    client = TestClient(timeout=1)

    with pytest.raises(httpx.TimeoutException):
        with client.session() as session:
            start = time.time()
            session.get('http://169.254.0.1')
            duration = time.time() - start
            assert 0.9 <= duration <= 1.1

@pytest.mark.asyncio
async def test_client_command_with_auth(test_server):
    """Test client command with authentication."""
    client = TestClient(
        'localhost',
        8000,
        'auth/42',
        username='username',
        password='password',
    )

    result = await client.example.test()
    assert result == b'{"foo": "bar"}'

    # Test session expiry
    await asyncio.sleep(2)
    result = await client.example.test()
    assert result == b'{"foo": "bar"}'

def test_server_reachability_scenarios():
    """Test various server reachability scenarios."""
    session = Mock(spec=httpx.Client)
    client = MockSessionClient(session)

    # Test successful connection
    assert client.is_server_reachable() is True

    # Test HTTP error (server is reachable but returns error)
    session.head.side_effect = HTTPError(Mock())
    assert client.is_server_reachable() is True

    # Test connection error
    session.head.side_effect = httpx.RequestError("Connection failed")
    assert client.is_server_reachable() is False

@pytest.mark.parametrize('tenant_id', [
    'my-tenant',
    UUID('550e8400-e29b-41d4-a716-446655440000'),
    None
])
def test_tenant_handling(tenant_id):
    """Test tenant ID handling."""
    client = TestClient()

    if tenant_id:
        client.tenant_uuid = tenant_id
        with client.session() as session:
            assert session.headers['Accent-Tenant'] == str(tenant_id)
    else:
        with client.session() as session:
            assert 'Accent-Tenant' not in session.headers
