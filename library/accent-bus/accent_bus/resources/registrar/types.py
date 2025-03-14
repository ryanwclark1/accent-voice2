# accent_bus/resources/registrar/types.py
# Copyright 2025 Accent Communications

"""Registrar types."""

from __future__ import annotations

from typing import TypedDict


class RegistrarDict(TypedDict, total=False):
    """Dictionary representing a registrar."""

    id: str
    deletable: bool
    name: str
    main_host: str
    main_port: int
    backup_host: str
    backup_port: int
    proxy_main_host: str
    proxy_main_port: int
    proxy_backup_host: str
    proxy_backup_port: int
    outbound_proxy_host: str
    outbound_proxy_port: int
