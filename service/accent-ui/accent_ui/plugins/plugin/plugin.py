# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint

from .service import PluginService
from .view import PluginView

plugin = create_blueprint('plugin', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        PluginView.service = PluginService(clients['accent_plugind'])
        PluginView.register(plugin, route_base='/plugins')
        register_flaskview(plugin, PluginView)

        core.register_blueprint(plugin)
