#!/usr/bin/env python3
# Copyright 2025 Accent Communications

"""Exceptions for the Accent Configuration Generator client."""


class ConfgendError(Exception):
    """Base exception for all confgend client errors."""



class ConfgendConnectionError(ConfgendError):
    """Exception raised when connection to the confgend server fails."""



class ConfgendTimeoutError(ConfgendError):
    """Exception raised when a request to the confgend server times out."""

