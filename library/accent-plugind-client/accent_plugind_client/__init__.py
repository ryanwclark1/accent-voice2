# Copyright 2025 Accent Communications

"""Accent Plugin Daemon client library.

This package provides a client for interacting with the Accent Plugin Daemon API,
supporting both synchronous and asynchronous operations.
"""

from .client import PlugindClient as Client
from .models import ConfigData, MarketData, PluginData, StatusData

__all__ = ["Client", "ConfigData", "MarketData", "PluginData", "StatusData"]
