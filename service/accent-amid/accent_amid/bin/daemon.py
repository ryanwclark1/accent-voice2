# src/accent_amid/bin/daemon.py
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging

from accent_amid.main import run_app

logger = logging.getLogger(__name__)


def main() -> None:
    """Entrypoint for the accent-amid daemon."""
    run_app()


if __name__ == "__main__":
    main()
