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

from .form import ParkingLotForm


class ParkingLotView(BaseIPBXHelperView):
    form = ParkingLotForm
    resource = 'parking_lot'

    @menu_item(
        '.ipbx.services.parkinglots',
        l_('Parking Lots'),
        icon="automobile",
        svg="M8.25 18.75a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 0 1-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 0 0-3.213-9.193 2.056 2.056 0 0 0-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 0 0-10.026 0 1.106 1.106 0 0 0-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12",
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _populate_form(self, form):
        form.music_on_hold.choices = self._build_set_choices_moh(form.music_on_hold)
        for form_extension in form.extensions:
            form_extension.context.choices = self._build_set_choices_context(
                form_extension
            )
        return form

    def _build_set_choices_moh(self, moh):
        if not moh.data or moh.data == 'None':
            return []
        moh_object = self.service.get_music_on_hold(moh.data)
        if moh_object is None:
            return []
        moh_label = moh_object['label']
        return [(moh.data, f"{moh_label} ({moh.data})")]

    def _build_set_choices_context(self, form):
        if not form.context.data or form.context.data == 'None':
            return []
        return [(form.context.data, form.context.data)]

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('parking_lot', {}))
        form.extensions[0].populate_errors(resources.get('extension', {}))
        return form

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['music_on_hold'] = self._convert_empty_string_to_none(
            form.music_on_hold.data
        )
        return resource


class ParkingLotDestinationView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        parking_lots = self.service.list(**params)
        results = [{'id': pl['id'], 'text': pl['name']} for pl in parking_lots['items']]
        return jsonify(build_select2_response(results, parking_lots['total'], params))
