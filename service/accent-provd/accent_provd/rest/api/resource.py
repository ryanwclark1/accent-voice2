# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

from twisted.web.static import File

if TYPE_CHECKING:
    from accent_provd.servers.http_site import Request


class ResponseFile(File):
    def render(self, request: Request) -> bytes:
        return File.render(self, request)

    def render_OPTIONS(self, request: Request) -> bytes:
        return b''
