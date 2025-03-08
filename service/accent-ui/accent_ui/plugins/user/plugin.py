# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.destination import register_destination_form
from accent_ui.helpers.funckey import register_funckey_destination_form
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .form import UserDestinationForm, UserFuncKeyDestinationForm
from .service import UserService
from .view import UserDestinationView, UserView

user = create_blueprint('user', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        UserView.service = UserService(clients['accent_confd'], clients['accent_auth'])
        UserView.register(user, route_base='/users')
        register_flaskview(user, UserView)

        UserDestinationView.service = UserService(
            clients['accent_confd'], clients['accent_auth']
        )
        UserDestinationView.register(user, route_base='/users_listing')

        register_destination_form('user', l_('User'), UserDestinationForm)
        register_funckey_destination_form(
            'user', l_('User'), UserFuncKeyDestinationForm
        )

        register_listing_url('user', 'user.UserDestinationView:list_json')
        register_listing_url('uuid_user', 'user.UserDestinationView:uuid_list_json')

        core.register_blueprint(user)
