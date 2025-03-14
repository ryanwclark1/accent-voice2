import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from example import app, RabbitMQConfig, get_rabbitmq_connection, Event
from unittest.mock import AsyncMock  # Import AsyncMock


# Example of overriding a dependency for testing.
@pytest.fixture
async def mock_rabbitmq_connection():
    """
    Fixture for mocking aiopika connection.
    """
    mock_connection = AsyncMock()
    mock_channel = AsyncMock()

    # Configure the mock connection to return the mock channel.
    mock_connection.channel.return_value = mock_channel

    # Async generator to be used with Depends()
    async def get_mock_connection():
        yield mock_connection

    return get_mock_connection


@pytest.fixture
def test_client(mock_rabbitmq_connection) -> TestClient:
    """
    Fixture to provide a test client that uses mocked services.
    Args:
        mock_rabbitmq_connection: Mocked aiopika connection.

    Returns:
        TestClient: Returns a test client.
    """
    app.dependency_overrides[get_rabbitmq_connection] = mock_rabbitmq_connection
    return TestClient(app)


@pytest.mark.asyncio
async def test_publish_event_success(
    test_client: TestClient,
    mock_rabbitmq_connection,
):
    """Test successful event publishing."""
    # Mock necessary methods on the channel.
    mock_exchange = AsyncMock()  # Use AsyncMock
    mock_rabbitmq_connection.return_value.channel.return_value.declare_exchange.return_value = mock_exchange

    test_event = Event(name="test_event", data={"key": "value"})
    response = test_client.post(
        "/publish/test_event",
        json=test_event.model_dump(),
    )
    assert response.status_code == 200
    assert response.json() == {"status": "published", "event": "test_event"}

    # Assert that publish was called.
    mock_exchange.publish.assert_awaited_once()


@pytest.mark.asyncio
async def test_publish_event_failure(test_client, mock_rabbitmq_connection):
    """Test event publishing failure due to exception."""

    # Mock the channel to raise an exception.
    mock_rabbitmq_connection.return_value.channel.return_value.declare_exchange.side_effect = Exception(
        "Mocked exception"
    )

    test_event = Event(name="test_event", data={"key": "value"})
    response = test_client.post(
        "/publish/test_event",
        json=test_event.model_dump(),
    )
    assert response.status_code == 500  # Expecting internal server error.


@pytest.mark.asyncio
async def test_subscribe_event_success(
    test_client: TestClient, mock_rabbitmq_connection
):
    """Test successful event subscription."""

    # Prepare the mock.
    mock_queue = AsyncMock()  # Use AsyncMock
    mock_rabbitmq_connection.return_value.channel.return_value.declare_queue.return_value = mock_queue
    mock_exchange = AsyncMock()  # Use AsyncMock
    mock_rabbitmq_connection.return_value.channel.return_value.declare_exchange.return_value = mock_exchange

    response = test_client.post("/subscribe/test_event")
    assert response.status_code == 200
    assert response.json()["status"] == "subscribed"
    assert "queue" in response.json()  # Check that queue is in response.

    # Assert that bind was called with correct arguments.
    mock_queue.bind.assert_awaited_once()


@pytest.mark.asyncio
async def test_subscribe_event_failure(test_client, mock_rabbitmq_connection):
    """Test failure during event subscription."""

    # Setup mock to simulate failure.
    mock_rabbitmq_connection.return_value.channel.return_value.declare_queue.side_effect = Exception(
        "Mocked exception"
    )

    response = test_client.post("/subscribe/test_event")
    assert response.status_code == 500  # Correctly check for 500 status code


@pytest.mark.asyncio
async def test_process_message_success(test_client):
    """Test successful message processing."""
    # Create a mock message (using a simple dict for demonstration)

    class MockMessage:
        """Mock AbstractIncomingMessage."""

        def __init__(self, body):
            self.body = body

        async def process(self):
            return self

        async def ack(self, **kwargs):
            pass

    valid_event_data = {"name": "valid_event", "data": {"key": "value"}}
    mock_message = MockMessage(
        body=Event(**valid_event_data).model_dump_json().encode()
    )

    # Call the function under test
    await process_message(mock_message)


@pytest.mark.asyncio
async def test_process_message_validation_error(test_client):
    """Test message processing with validation error."""

    # Create a mock message with invalid data
    class MockMessage:
        """Mock AbstractIncomingMessage."""

        def __init__(self, body):
            self.body = body

        async def process(self):
            return self

        async def ack(self, **kwargs):
            pass

    invalid_event_data = {"name": 123, "data": "not a dict"}  # Invalid data
    mock_message = MockMessage(
        body=Event(**invalid_event_data).model_dump_json().encode()
        if isinstance(invalid_event_data, dict)
        else json.dumps(invalid_event_data).encode()
    )

    # Call the function under test
    await process_message(mock_message)


@pytest.mark.asyncio
async def test_config_url():
    """Test RabbitMQConfig URL."""
    config = RabbitMQConfig(
        user="testuser", password="testpassword", host="testhost", port=1234
    )
    assert config.url == "amqp://testuser:testpassword@testhost:1234/"

    default_config = RabbitMQConfig()
    assert default_config.url == "amqp://guest:guest@localhost:5672/"
