# Copyright 2023 Accent Communications

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, TypeVar

from accent.auth_verifier import required_acl as required_acl_
from accent.auth_verifier import required_tenant
from werkzeug.local import LocalProxy as Proxy

from .exceptions import NotInitializedException
from .rest_api import app

if TYPE_CHECKING:
    from accent_auth_client.types import TokenDict

    F = TypeVar('F')

required_acl = required_acl_


def required_master_tenant() -> Callable[[F], F]:
    return required_tenant(master_tenant_uuid)


def init_master_tenant(token: TokenDict) -> None:
    tenant_uuid = token['metadata']['tenant_uuid']
    app.config['auth']['master_tenant_uuid'] = tenant_uuid


def get_master_tenant_uuid() -> str:
    if not app:
        raise Exception('Flask application not configured')

    tenant_uuid = app.config['auth'].get('master_tenant_uuid')
    if not tenant_uuid:
        raise NotInitializedException()
    return tenant_uuid


master_tenant_uuid = Proxy(get_master_tenant_uuid)
