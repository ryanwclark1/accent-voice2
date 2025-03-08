# Copyright 2023 Accent Communications

from flask import flash, render_template
from flask_babel import gettext as _
from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError

from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.view import BaseIPBXHelperView

from .form import RtpForm


class RtpView(BaseIPBXHelperView):
    form = RtpForm
    resource = 'rtp'

    @menu_item('.ipbx.global_settings.rtp', l_('Rtp'), icon="volume-off", svg="M17.25 9.75 19.5 12m0 0 2.25 2.25M19.5 12l2.25-2.25M19.5 12l-2.25 2.25m-10.5-6 4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z")
    def index(self):
        try:
            resource = self.service.get()
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        return render_template(
            self._get_template('index'), form=self.form(data=resource['options'])
        )

    def post(self):
        form = self.form()
        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self._index(form)

        resource = form.to_dict()

        try:
            self.service.update(resource)
        except HTTPError as error:
            self._flash_http_error(error)
            return self.index()

        flash(_('RTP config has been updated'), 'success')
        return self._redirect_for('index')
