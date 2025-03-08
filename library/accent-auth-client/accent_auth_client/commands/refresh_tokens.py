# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import Any

from accent_lib_rest_client import RESTCommand

from ..types import JSON


class RefreshTokenCommand(RESTCommand):
    resource = 'tokens'

    def list(self, **kwargs: Any) -> JSON:
        headers = self._get_headers(**kwargs)
        r = self.session.get(self.base_url, headers=headers, params=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()
