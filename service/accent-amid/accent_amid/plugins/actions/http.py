# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import Any

import requests
from flask import request

from accent_amid.ami import parser
from accent_amid.auth import required_acl, required_master_tenant
from accent_amid.plugin_helpers.ajam import AJAMClient, AJAMUnreachable
from accent_amid.rest_api import AuthResource

from .exceptions import UnsupportedAction


class ActionResource(AuthResource):
    def __init__(self, ajam_client: AJAMClient) -> None:
        self.ajam_client = ajam_client

    @required_master_tenant()
    @required_acl('amid.action.{action}.create')
    def post(self, action: str) -> tuple[list[dict[str, Any]], int]:
        if action.lower() in ('queues', 'command'):
            raise UnsupportedAction(action)

        extra_args = request.get_json(force=True, silent=True) or {}

        try:
            response = self.ajam_client.get(action, extra_args)
        except requests.RequestException as e:
            raise AJAMUnreachable(self.ajam_client.url, e)

        return self._parse_ami(response.content), 200

    @staticmethod
    def _parse_ami(buffer_: bytes) -> list[dict[str, Any]]:
        result = []

        def aux(
            event_name: str, action_id: str | None, message: dict[str, Any]
        ) -> None:
            result.append(message)

        parser.parse_buffer(buffer_, aux, aux)

        return result
