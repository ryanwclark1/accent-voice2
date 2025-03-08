# Copyright 2023 Accent Communications

from __future__ import annotations

import requests
from flask import request

from accent_amid.ami import parser
from accent_amid.auth import required_acl, required_master_tenant
from accent_amid.plugin_helpers.ajam import AJAMClient, AJAMUnreachable
from accent_amid.rest_api import AuthResource

from .schema import command_schema


class CommandResource(AuthResource):
    def __init__(cls, ajam_client: AJAMClient) -> None:
        cls.ajam_client = ajam_client

    @required_master_tenant()
    @required_acl('amid.action.Command.create')
    def post(self) -> tuple[dict[str, list[str]], int]:
        extra_args = command_schema.load(request.get_json(force=True))
        try:
            response = self.ajam_client.get('Command', extra_args)
        except requests.RequestException as e:
            raise AJAMUnreachable(self.ajam_client.url, e)

        response_lines = self._parse_ami_command(response.content)
        return {'response': response_lines}, 200

    @staticmethod
    def _parse_ami_command(command_result: bytes) -> list[str]:
        return parser.parse_command_response(command_result)
