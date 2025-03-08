# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.funckey import register_funckey_destination_form
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .form import CallFilterFuncKeyDestinationForm
from .service import CallFilterService
from .view import CallFilterMemberListingView, CallFilterView

call_filter = create_blueprint('call_filter', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        CallFilterView.service = CallFilterService(clients['accent_confd'])
        CallFilterView.register(call_filter, route_base='/callfilters')
        register_flaskview(call_filter, CallFilterView)

        CallFilterMemberListingView.service = CallFilterService(clients['accent_confd'])
        CallFilterMemberListingView.register(
            call_filter, route_base='/callfilters_listing'
        )

        register_funckey_destination_form(
            'bsfilter', l_('Call Filter'), CallFilterFuncKeyDestinationForm
        )
        register_listing_url(
            'bsfilter', 'call_filter.CallFilterMemberListingView:list_json'
        )

        core.register_blueprint(call_filter)
