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

from .form import ApplicationForm


class ApplicationView(BaseIPBXHelperView):
    form = ApplicationForm
    resource = 'application'

    @menu_item(
        '.ipbx.services.applications',
        l_('Applications'),
        icon="cubes",
        svg="m6.75 7.5 3 2.25-3 2.25m4.5 0h3m-9 8.25h13.5A2.25 2.25 0 0 0 21 18V6a2.25 2.25 0 0 0-2.25-2.25H5.25A2.25 2.25 0 0 0 3 6v12a2.25 2.25 0 0 0 2.25 2.25Z",
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        # TODO should be in the ApplicationDestinationForm
        destination = resource.pop('destination_options')
        destination['destination'] = resource.pop('destination') or 'None'
        form = self.form(data=resource, destination=destination)
        return form

    def _map_form_to_resources(self, form, form_id=None):
        # TODO should be in the ApplicationDestinationForm
        resource = form.to_dict()
        if form_id:
            resource['uuid'] = form_id
        resource['destination_options'] = resource.pop('destination')
        resource['destination'] = resource['destination_options'].pop('destination')
        return resource


class ApplicationDestinationView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        applications = self.service.list()
        results = []
        for application in applications['items']:
            results.append({'id': application['uuid'], 'text': application['name']})

        return jsonify(build_select2_response(results, applications['total'], params))
