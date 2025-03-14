# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import LineService
from .view import LineListingView, LineView

line = create_blueprint('line', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        LineView.service = LineService(clients['accent_confd'])
        LineView.register(line, route_base='/lines')
        register_flaskview(line, LineView)

        LineListingView.service = LineService(clients['accent_confd'])
        LineListingView.register(line, route_base='/lines_listing')

        register_listing_url('line', 'line.LineListingView:list_json')

        core.register_blueprint(line)
