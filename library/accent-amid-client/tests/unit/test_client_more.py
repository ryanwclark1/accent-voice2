# tests/unit/test_client_more.py
import pytest
from accent_amid_client.client import AmidClient


def test_amid_client_init_with_kwargs(mocker):
    """Test AmidClient initialization with extra kwargs."""
    mock_super_init = mocker.patch("accent_lib_rest_client.client.BaseClient.__init__")
    client = AmidClient(host="example.com", port=1234, timeout=30, verify=False)
    mock_super_init.assert_called_once_with(
        host="example.com",
        port=1234,
        prefix="/api/amid",
        version="1.0",
        timeout=30,
        verify=False,
    )

