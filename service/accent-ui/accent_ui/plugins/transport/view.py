# Copyright 2023 Accent Communications

import logging

from flask import jsonify, request
from flask_babel import lazy_gettext as l_

from accent_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params,
)
from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.view import BaseIPBXHelperView, NewHelperViewMixin

from .form import TransportForm

logger = logging.getLogger(__name__)


class TransportView(NewHelperViewMixin, BaseIPBXHelperView):
    form = TransportForm
    resource = 'transport'

    @menu_item(
        '.ipbx.global_settings.transports',
        l_('PJSIP Transports'),
        icon="asterisk",
        svg="M8.25 18.75a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 0 1-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 0 0-3.213-9.193 2.056 2.056 0 0 0-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 0 0-10.026 0 1.106 1.106 0 0 0-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12",
        multi_tenant=False,
    )
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        options = [
            {
                'option_key': option[0],
                'option_value': option[1],
            }
            for option in resource['options']
        ]
        choices = [(key, key) for key, _ in resource['options']]

        form = self.form(
            id=resource['uuid'],
            data=resource,
            name=resource['name'],
            options=options,
        )

        # Use all the current options for the choices, the complete list will be pulled on edit
        for option in form.options:
            option.option_key.choices = choices

        return form

    def _map_form_to_resources(self, form, form_id=None):
        data = super()._map_form_to_resources(form, form_id)
        data['options'] = [
            [opt['option_key'], opt['option_value']] for opt in data['options']
        ]
        return data


class TransportDestinationView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        transports = self.service.list(**params)
        results = [{'id': t['uuid'], 'text': t['name']} for t in transports['items']]
        return jsonify(build_select2_response(results, transports['total'], params))
