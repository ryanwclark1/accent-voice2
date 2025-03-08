# Copyright 2023 Accent Communications

from __future__ import annotations

from accent_lib_rest_client import RESTCommand

from ..types import JSON


class ConfigCommand(RESTCommand):
    resource = 'config'

    def get(self) -> JSON:
        headers = self._get_headers()
        r = self.session.get(self.base_url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def patch(self, config_patch: dict[str, JSON]) -> JSON:
        headers = self._get_headers()
        r = self.session.patch(self.base_url, headers=headers, json=config_patch)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
