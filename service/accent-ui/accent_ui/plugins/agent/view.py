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

from .form import AgentForm


class AgentView(BaseIPBXHelperView):
    form = AgentForm
    resource = 'agent'
    raw_skills = []

    @menu_item('.ipbx.callcenter.agents', l_('Agents'), icon="users", svg='M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z', multi_tenant=True)
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        # Trick to store ids and names directly and map them in _populate_form,
        # because wtforms will map name to `skill-0` ...
        self.raw_skills = resource['skills']

        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        for idx, raw_skill in enumerate(self.raw_skills):
            form.skills[idx].skill_id.choices = [(raw_skill['id'], raw_skill['name'])]

        return form


class AgentListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        agents = self.service.list(**params)
        results = [
            {'id': agent['id'], 'text': agent['number']} for agent in agents['items']
        ]
        return jsonify(build_select2_response(results, agents['total'], params))
