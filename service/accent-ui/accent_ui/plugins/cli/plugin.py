# Copyright 2023 Accent Communications


from flask import render_template
from wtforms.fields import StringField, SubmitField
from wtforms.validators import InputRequired, Length

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.form import BaseForm
from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import BaseIPBXHelperView

asterisk_cli = create_blueprint('asterisk_cli', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        AsteriskCliView.service = AsteriskCliService(clients['accent_amid'])
        AsteriskCliView.register(asterisk_cli, route_base='/asterisk_cli')
        register_flaskview(asterisk_cli, AsteriskCliView)

        core.register_blueprint(asterisk_cli)


class AsteriskCliForm(BaseForm):
    command = StringField('Command', [InputRequired, Length(max=128)])
    submit = SubmitField('Submit')


class AsteriskCliView(BaseIPBXHelperView):
    form = AsteriskCliForm
    resource = 'asterisk_cli'

    @menu_item('.ipbx.global_settings.asterisk_cli', 'Asterisk CLI', icon="terminal", svg="m6.75 7.5 3 2.25-3 2.25m4.5 0h3m-9 8.25h13.5A2.25 2.25 0 0 0 21 18V6a2.25 2.25 0 0 0-2.25-2.25H5.25A2.25 2.25 0 0 0 3 6v12a2.25 2.25 0 0 0 2.25 2.25Z")
    def index(self):
        return render_template(
            self._get_template('list'), form=self._populate_form(self.form())
        )

    def post(self):
        resources = self._map_form_to_resources_post(self.form())
        data = self.service.send_cmd(resources.get('command'))
        return render_template(
            self._get_template('list'),
            form=self._populate_form(self.form()),
            results=data,
        )


class AsteriskCliService:
    def __init__(self, amid_client):
        self._amid = amid_client

    def send_cmd(self, cmd):
        return self._amid.command(cmd)['response']
