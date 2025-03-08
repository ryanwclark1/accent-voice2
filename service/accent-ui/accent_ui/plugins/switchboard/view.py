# Copyright 2023 Accent Communications

from flask import jsonify, request
from flask_babel import lazy_gettext as l_

from accent_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params,
)
from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.view import BaseIPBXHelperView

from .form import SwitchboardForm


class SwitchboardView(BaseIPBXHelperView):
    form = SwitchboardForm
    resource = 'switchboard'

    @menu_item(
        '.ipbx.services.switchboards',
        l_('Switchboards'),
        icon="desktop",
        svg="M9 17.25v1.007a3 3 0 0 1-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0 1 15 18.257V17.25m6-12V15a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 15V5.25m18 0A2.25 2.25 0 0 0 18.75 3H5.25A2.25 2.25 0 0 0 3 5.25m18 0V12a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 12V5.25",
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        users = [user['uuid'] for user in resource['members']['users']]
        resource['members']['user_uuids'] = users
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.members.user_uuids.choices = self._build_set_choices_users(
            form.members.users
        )
        form.queue_music_on_hold.choices = self._build_set_choices_moh(
            form.queue_music_on_hold
        )
        form.waiting_room_music_on_hold.choices = self._build_set_choices_moh(
            form.waiting_room_music_on_hold
        )
        return form

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            if user.lastname.data:
                text = f'{user.firstname.data} {user.lastname.data}'
            else:
                text = user.firstname.data
            results.append((user.uuid.data, text))
        return results

    def _build_set_choices_moh(self, moh):
        if not moh.data or moh.data == 'None':
            return []
        moh_object = self.service.get_music_on_hold(moh.data)
        if moh_object is None:
            return []
        moh_label = moh_object['label']
        return [(moh.data, f"{moh_label} ({moh.data})")]

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['members']['users'] = [
            {'uuid': user_uuid} for user_uuid in form.members.user_uuids.data
        ]
        resource['queue_music_on_hold'] = self._convert_empty_string_to_none(
            form.queue_music_on_hold.data
        )
        resource['waiting_room_music_on_hold'] = self._convert_empty_string_to_none(
            form.waiting_room_music_on_hold.data
        )

        return resource

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('switchboard', {}))
        return form


class SwitchboardDestinationView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        switchboards = self.service.list(**params)
        results = [
            {'id': sw['uuid'], 'text': sw['name']} for sw in switchboards['items']
        ]
        return jsonify(build_select2_response(results, switchboards['total'], params))
