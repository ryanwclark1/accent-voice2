# Copyright 2023 Accent Communications

from __future__ import annotations

from accent.status import StatusAggregator

_STATUS_AGGREGATOR: StatusAggregator = StatusAggregator()


def get_status_aggregator():
    global _STATUS_AGGREGATOR
    return _STATUS_AGGREGATOR
