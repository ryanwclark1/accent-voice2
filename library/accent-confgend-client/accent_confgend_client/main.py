#!/usr/bin/env python3
# Copyright 2025 Accent Communications

"""Main entry point for the Accent Configuration Generator client.

This module provides backward compatibility with the original script.
"""

import sys

from accent_confgend_client.cli import main

if __name__ == "__main__":
    sys.exit(main())
