# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import CallPermissionService
from .view import CallPermissionListingView, CallPermissionView

call_permission = create_blueprint('call_permission', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        CallPermissionView.service = CallPermissionService(clients['accent_confd'])
        CallPermissionView.register(call_permission, route_base='/callpermissions')
        register_flaskview(call_permission, CallPermissionView)

        CallPermissionListingView.service = CallPermissionService(clients['accent_confd'])
        CallPermissionListingView.register(
            call_permission, route_base='/callpermissions_listing'
        )

        register_listing_url(
            'callpermission', 'call_permission.CallPermissionListingView:list_json'
        )

        core.register_blueprint(call_permission)
