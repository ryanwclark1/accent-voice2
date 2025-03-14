# Copyright 2023 Accent Communications

from __future__ import annotations

import string

from .common import CollectdEvent


def _validate_plugin_instance_fragment(plugin_instance_fragment: str) -> str:
    result = ''.join(
        c
        for c in plugin_instance_fragment
        if (c in string.ascii_letters or c in string.digits or c == '-')
    )
    return result or '<unknown>'


class _BaseCallCollectdEvent(CollectdEvent):
    routing_key_fmt = 'collectd.calls'
    plugin = 'calls'
    type_ = 'counter'
    values = ('1',)

    def __init__(
        self,
        application: str,
        application_id: str | None,
        time: int | str | None = None,
    ):
        super().__init__()
        if time:
            self.time = int(time)

        application = _validate_plugin_instance_fragment(application)
        if application_id is not None:
            application_id = _validate_plugin_instance_fragment(application_id)
            self.plugin_instance = f'{application}.{application_id}'
        else:
            self.plugin_instance = application


class CallStartCollectdEvent(_BaseCallCollectdEvent):
    name = 'collectd_call_started'
    type_instance = 'start'


class CallConnectCollectdEvent(_BaseCallCollectdEvent):
    name = 'collectd_call_connected'
    type_instance = 'connect'


class CallEndCollectdEvent(_BaseCallCollectdEvent):
    name = 'collectd_call_ended'
    type_instance = 'end'


class CallAbandonedCollectdEvent(_BaseCallCollectdEvent):
    name = 'collectd_call_abandoned'
    type_instance = 'abandoned'


class CallDurationCollectdEvent(_BaseCallCollectdEvent):
    name = 'collectd_call_duration'
    type_ = 'gauge'
    type_instance = 'duration'

    def __init__(
        self,
        application: str,
        application_id: str | None,
        duration: int,
        time: str | int | None = None,
    ):
        super().__init__(application, application_id, time)
        self.values = (str(round(duration, 3)),)
