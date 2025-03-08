# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.funckey import register_funckey_destination_form
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .form import ParkingFuncKeyDestinationForm, ParkPositionFuncKeyDestinationForm
from .service import ParkingLotService
from .view import ParkingLotDestinationView, ParkingLotView

parking_lot = create_blueprint('parking_lot', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        ParkingLotView.service = ParkingLotService(clients['accent_confd'])
        ParkingLotView.register(parking_lot, route_base='/parkinglots')
        register_flaskview(parking_lot, ParkingLotView)

        ParkingLotDestinationView.service = ParkingLotService(clients['accent_confd'])
        ParkingLotDestinationView.register(
            parking_lot, route_base='/parking_lot_destination'
        )

        register_funckey_destination_form(
            'parking', l_('Parking'), ParkingFuncKeyDestinationForm
        )
        register_funckey_destination_form(
            'park_position', l_('Parking Position'), ParkPositionFuncKeyDestinationForm
        )
        register_listing_url(
            'parking', 'parking_lot.ParkingLotDestinationView:list_json'
        )
        register_listing_url(
            'park_position', 'parking_lot.ParkingLotDestinationView:list_json'
        )

        core.register_blueprint(parking_lot)
