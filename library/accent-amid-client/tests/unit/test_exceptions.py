# tests/unit/test_exceptions.py
import pytest
import httpx
from accent_amid_client.exceptions import (
    AmidError,
    AmidProtocolError,
    AmidServiceUnavailable,
    InvalidAmidError,
)


def test_amid_error():
    """Test the AmidError exception."""
    response = httpx.Response(
        400,
        json={
            "message": "Test Error",
            "error_id": "123",
            "details": "Some details",
            "timestamp": "now",
            "resource": "test",
        },
        request=httpx.Request('GET', 'http://example.com')
    )
    error = AmidError(response)
    assert str(error) == "Test Error: Some details"
    assert error.status_code == 400
    assert error.message == "Test Error"
    assert error.error_id == "123"
    assert error.details == "Some details"
    assert error.timestamp == "now"
    assert error.resource == "test"


def test_amid_error_missing_fields():
    """Test AmidError with missing fields in the response."""
    response = httpx.Response(400, json={"message": "Test Error"}, request=httpx.Request('GET', 'http://example.com'))
    with pytest.raises(InvalidAmidError):
        AmidError(response)


def test_amid_error_invalid_json():
    """Test AmidError with invalid JSON in the response."""
    response = httpx.Response(400, content=b"invalid json", request=httpx.Request('GET', 'http://example.com'))
    with pytest.raises(InvalidAmidError):
        AmidError(response)


def test_amid_service_unavailable():
    """Test the AmidServiceUnavailable exception."""
    response = httpx.Response(
        503,
        json={
            "message": "Service Unavailable",
            "error_id": "503",
            "details": "Server down",
            "timestamp": "now",
        },
        request=httpx.Request('GET', 'http://example.com')
    )
    error = AmidServiceUnavailable(response)
    assert str(error) == "Service Unavailable: Server down"
    assert error.status_code == 503


def test_amid_protocol_error():
    """Test the AmidProtocolError exception."""
    response = httpx.Response(200, json=[{"Response": "Error", "Message": "Test Protocol Error"}], request=httpx.Request('GET', 'http://example.com'))
    error = AmidProtocolError(response)
    assert str(error) == "Test Protocol Error"
    assert error.status_code == 200
    assert error.message == "Test Protocol Error"



def test_amid_protocol_error_invalid_format():
    """Test AmidProtocolError with an invalid error format."""
    response = httpx.Response(200, json=[{"Invalid": "Error"}], request=httpx.Request('GET', 'http://example.com'))
    with pytest.raises(