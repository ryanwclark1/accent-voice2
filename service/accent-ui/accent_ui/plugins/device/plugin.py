# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import DeviceService
from .view import DeviceListingView, DeviceView

device = create_blueprint('device', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        DeviceView.service = DeviceService(clients['accent_confd'], clients['accent_provd'])
        DeviceView.register(device, route_base='/devices')
        register_flaskview(device, DeviceView)

        DeviceListingView.service = DeviceService(
            clients['accent_confd'], clients['accent_provd']
        )
        DeviceListingView.register(device, route_base='/devices_listing')

        register_listing_url('device', 'device.DeviceListingView:list_json')

        core.register_blueprint(device)
