# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import ScheduleService
from .view import ScheduleListingView, ScheduleView

schedule = create_blueprint('schedule', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        ScheduleView.service = ScheduleService(clients['accent_confd'])
        ScheduleView.register(schedule, route_base='/schedules')
        register_flaskview(schedule, ScheduleView)

        ScheduleListingView.service = ScheduleService(clients['accent_confd'])
        ScheduleListingView.register(schedule, route_base='/schedules_listing')

        register_listing_url('schedule', 'schedule.ScheduleListingView:list_json')

        core.register_blueprint(schedule)
