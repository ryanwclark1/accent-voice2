# tests/test_base.py
import logging

import pytest
from accent_bus.base import Base, ConnectionParams


@pytest.fixture
def base_instance():
    return Base(name="TestBase")


def test_base_initialization(base_instance):
    """Test the initialization of the Base class."""
    assert base_instance._name == "TestBase"
    assert isinstance(base_instance._logger, logging.Logger)
    assert base_instance._connection_params == ConnectionParams(
        "guest", "guest", "localhost", 5672
    )
    assert base_instance._default_exchange_name == ""
    assert base_instance._default_exchange_type == ""


def test_url_property(base_instance):
    """Test the url property."""
    assert base_instance.url == "amqp://guest:guest@localhost:5672/"


def test_log_property(base_instance):
    """Test the log property."""
    assert base_instance.log == base_instance._logger  # Corrected attribute name


@pytest.mark.asyncio
async def test_is_running_property(base_instance):
    """Test the is_running property."""
    assert await base_instance.is_running == True


@pytest.mark.asyncio
async def test_base_aenter(base_instance):
    """Test __aenter__."""
    async with base_instance as b:
        assert b == base_instance
        assert await b.is_running


@pytest.mark.asyncio
async def test_base_aexit(base_instance):
    """Test __aexit__."""
    async with base_instance as b:
        pass  # No-op inside the context
    # In Base __aexit__ doesn't have logic, but good practice to have a test.
