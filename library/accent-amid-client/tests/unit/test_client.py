# tests/unit/test_client.py
import pytest
from accent_amid_client.client import AmidClient


def test_client_initialization(mock_server: str):
    """Test that the client initializes correctly."""
    client = AmidClient(host=mock_server, port=80)
    assert client.base_url == f"{mock_server}/api/amid/1.0"
    assert client.sync_client is not None
    assert client.async_client is not None

    client = AmidClient(host=mock_server, port=8080, prefix="/custom", version="2.0")
    assert client.base_url == f"{mock_server}:8080/custom/2.0"
