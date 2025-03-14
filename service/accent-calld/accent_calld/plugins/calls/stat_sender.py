# Copyright 2023 Accent Communications

import logging

from accent_bus.collectd.calls import (
    CallAbandonedCollectdEvent,
    CallConnectCollectdEvent,
    CallDurationCollectdEvent,
    CallEndCollectdEvent,
    CallStartCollectdEvent,
)

logger = logging.getLogger(__name__)


class StatSender:
    def __init__(self, collectd):
        self.collectd = collectd

    def new_call(self, call):
        logger.debug('sending stat for new call %s', call.channel.id)
        self.collectd.publish_soon(CallStartCollectdEvent(call.app, call.app_instance))

    def abandoned(self, call):
        logger.debug('sending stat for abandoned call %s', call.channel.id)
        self.collectd.publish_soon(
            CallAbandonedCollectdEvent(call.app, call.app_instance)
        )

    def duration(self, call):
        logger.debug('sending stat for duration of call %s', call.channel.id)
        self.collectd.publish_soon(
            CallDurationCollectdEvent(call.app, call.app_instance, call.duration())
        )

    def connect(self, call):
        logger.debug('sending stat for connecting call %s', call.channel.id)
        self.collectd.publish_soon(
            CallConnectCollectdEvent(call.app, call.app_instance)
        )

    def end_call(self, call):
        logger.debug('sending stat for ended call %s', call.channel.id)
        self.collectd.publish_soon(CallEndCollectdEvent(call.app, call.app_instance))
