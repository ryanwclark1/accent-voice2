# Copyright 2023 Accent Communications

from accent_ui.helpers.plugin import create_blueprint_core as create_blueprint

from .view import Login, Logout

login = create_blueprint('login', __name__)
logout = create_blueprint('logout', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        Login.babel = core.babel_instance
        Login.register(login, route_base='/login', route_prefix='')
        core.register_blueprint(login)

        Logout.auth_client = clients['accent_auth']
        Logout.register(logout, route_base='/logout', route_prefix='')
        core.register_blueprint(logout)
