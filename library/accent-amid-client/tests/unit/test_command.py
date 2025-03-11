# tests/unit/test_command_base.py

import pytest
import httpx
from accent_amid_client.command import AmidCommand
from accent_amid_client.exceptions import (
    AmidError,
    AmidProtocolError,
    AmidServiceUnavailable,
    InvalidAmidError,
)


def test_raise_from_response_503(mock_503_response):
    """Test that a 503 response raises AmidServiceUnavailable."""
    with pytest.raises(AmidServiceUnavailable):
        AmidCommand.raise_from_response(httpx.Response(503))


def test_raise_from_response_amid_error(mock_400_response):
    with pytest.raises(AmidError) as excinfo:
        AmidCommand.raise_from_response(
            httpx.Response(
                400,
                json={
                    "message": "Bad Request",
                    "error_id": "ID123",
                    "details": "Invalid input",
                    "timestamp": "2024-07-30T12:00:00Z",
                },
            )
        )
    assert str(excinfo.value) == "Bad Request: Invalid input"
    assert excinfo.value.error_id == "ID123"


def test_raise_from_response_invalid_amid_error(mock_invalid_amid_response):
    """Test that an invalid AMID error response falls back to RESTCommand.raise_from_response."""
    with pytest.raises(httpx.HTTPStatusError):  # Expecting the base class exception
        AmidCommand.raise_from_response(
            httpx.Response(400, json={"invalid": "response"})
        )


def test_raise_from_response_invalid_json(mock_invalid_json_response):
    """Test handling of invalid JSON in an error response."""
    with pytest.raises(httpx.HTTPStatusError):  # Expecting base class error handling
        AmidCommand.raise_from_response(httpx.Response(200, content="invalid json"))


def test_raise_from_protocol_error(mock_protocol_error):
    """Test that a protocol error raises AmidProtocolError."""
    with pytest.raises(AmidProtocolError) as excinfo:
        AmidCommand.raise_from_protocol(
            httpx.Response(
                200, json=[{"Response": "Error", "Message": "Protocol Error"}]
            )
        )
    assert str(excinfo.value) == "Protocol Error"


def test_raise_from_protocol_invalid_error(mock_invalid_protocol_error):
    """Test that an invalid protocol error format falls back to RESTCommand."""
    with pytest.raises(httpx.HTTPStatusError):
        AmidCommand.raise_from_protocol(
            httpx.Response(200, json=[{"Invalid": "Error"}])
        )


def test_raise_from_protocol_invalid_json(mock_invalid_json_response):
    with pytest.raises(httpx.HTTPStatusError):
        AmidCommand.raise_from_protocol(httpx.Response(200, content="invalid json"))
