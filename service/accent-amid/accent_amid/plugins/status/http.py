# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

from accent.auth_verifier import required_acl

from accent_amid.rest_api import AuthResource

if TYPE_CHECKING:
    from accent.status import StatusAggregator, StatusDict


class StatusResource(AuthResource):
    def __init__(self, status_aggregator: StatusAggregator) -> None:
        self.status_aggregator = status_aggregator

    @required_acl('amid.status.read')
    def get(self) -> tuple[StatusDict, int]:
        return self.status_aggregator.status(), 200
