# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from accent.auth_verifier import required_acl

from accent_webhookd.rest_api import AuthResource

if TYPE_CHECKING:
    from stevedore import NamedExtensionManager


class ServicesDict(TypedDict):
    services: dict[str, dict]


class ServicesResource(AuthResource):
    def __init__(self, service_manager: NamedExtensionManager) -> None:
        self._service_manager = service_manager

    @required_acl('webhookd.subscriptions.services.read')
    def get(self) -> tuple[ServicesDict, int]:
        result: ServicesDict = {
            'services': {name: {} for name in self._service_manager.names()}
        }
        return result, 200
