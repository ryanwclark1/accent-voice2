from collections.abc import Callable
from typing import Any, TypedDict

from accent.status import StatusAggregator
from accent.token_renewer import Callback
from accent_auth_client import Client as AuthClient
from flask_restful import Api

from accent_confd._bus import BusConsumer, BusPublisher
from accent_confd.helpers.asterisk import PJSIPDoc
from accent_confd.helpers.middleware import MiddleWareHandle

TokenChangedSubscribeCallback = Callable[[Callback], None]


class PluginDependencies(TypedDict):
    api: Api
    config: dict[str, Any]
    token_changed_subscribe: TokenChangedSubscribeCallback
    bus_consumer: BusConsumer
    bus_publisher: BusPublisher
    auth_client: AuthClient
    middleware_handle: MiddleWareHandle
    pjsip_doc: PJSIPDoc
    status_aggregator: StatusAggregator
