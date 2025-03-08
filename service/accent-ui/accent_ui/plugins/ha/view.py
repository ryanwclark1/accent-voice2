# Copyright 2023 Accent Communications

from flask import flash, render_template
from flask_babel import gettext as _
from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError

from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.view import BaseIPBXHelperView

from .form import HaForm


class HaView(BaseIPBXHelperView):
    form = HaForm
    resource = 'ha'

    @menu_item(
        '.ipbx.global_settings.ha',
        l_('High Availability'),
        order=2,
        icon="balance-scale",
        svg="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0 0 12 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52 2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 0 1-2.031.352 5.988 5.988 0 0 1-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971Zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0 2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 0 1-2.031.352 5.989 5.989 0 0 1-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971Z",
    )
    def index(self):
        try:
            resource = self.service.get()
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        return render_template(
            self._get_template('index'), form=self.form(data=resource)
        )

    def post(self):
        form = self.form()
        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self.index()

        resource = form.to_dict()

        try:
            self.service.update(resource)
        except HTTPError as error:
            self._flash_http_error(error)
            return self.index()

        flash(_('High Availabitity config has been updated'), 'success')
        return self._redirect_for('index')
