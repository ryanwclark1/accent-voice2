# src/accent_chatd/plugins/config/plugin.py
from accent_chatd.core.plugin import Plugin  # Import the base class
from .http import ConfigResource


class Plugin(Plugin):
    def load(self, dependencies):
        config = dependencies["config"]
        api = dependencies["app"]
        api.add_api_route(
            "/config", ConfigResource(config).get, methods=["GET"], tags=["config"]
        )
        api.add_api_route(
            "/config", ConfigResource(config).patch, methods=["PATCH"], tags=["config"]
        )