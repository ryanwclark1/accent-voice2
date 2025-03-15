# src/accent_chatd/plugins/api/plugin.py
from accent_chatd.core.plugin import Plugin
from .http import SwaggerResource


class Plugin(Plugin):  # Inherit
    def load(self, dependencies):
        api = dependencies["app"]
        api.add_api_route("/api/api.yml", SwaggerResource().get)
