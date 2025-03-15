# src/accent_chatd/plugins/status/plugin.py

from accent.status import Status
from accent_chatd.core.plugin import Plugin

from .resource import StatusResource


class Plugin(Plugin):  # Inherit
    def load(self, dependencies):
        # status_aggregator = dependencies['status_aggregator']

        # status_aggregator.add_provider(provide_status) # Not using now.
        api = dependencies["app"]
        api.add_api_route(
            "/status", StatusResource(None).get, methods=["GET"], tags=["status"]
        )  # Removed status_aggregator


def provide_status(status):  # Not using
    status["rest_api"]["status"] = Status.ok
