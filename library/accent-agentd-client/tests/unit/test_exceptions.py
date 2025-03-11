# tests/unit/test_exceptions.py
import pytest
from accent_agentd_client.error import AgentdClientError, NO_SUCH_AGENT


def test_agentd_client_error() -> None:
    """Tests the AgentdClientError exception."""
    error_message = "Test error message"
    with pytest.raises(AgentdClientError) as excinfo:
        raise AgentdClientError(error_message)
    assert str(excinfo.value) == error_message
    assert excinfo.value.error == error_message


def test_predefined_errors() -> None:
    """Tests that the predefined error constants are strings."""
    assert isinstance(NO_SUCH_AGENT, str)
    # Add similar assertions for other error constants if needed
