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

from .form import QueueForm


class QueueView(BaseIPBXHelperView):
    form = QueueForm
    resource = 'queue'

    @menu_item('.ipbx.callcenter', l_('Call Center'), icon="support", svg="M16.712 4.33a9.027 9.027 0 0 1 1.652 1.306c.51.51.944 1.064 1.306 1.652M16.712 4.33l-3.448 4.138m3.448-4.138a9.014 9.014 0 0 0-9.424 0M19.67 7.288l-4.138 3.448m4.138-3.448a9.014 9.014 0 0 1 0 9.424m-4.138-5.976a3.736 3.736 0 0 0-.88-1.388 3.737 3.737 0 0 0-1.388-.88m2.268 2.268a3.765 3.765 0 0 1 0 2.528m-2.268-4.796a3.765 3.765 0 0 0-2.528 0m4.796 4.796c-.181.506-.475.982-.88 1.388a3.736 3.736 0 0 1-1.388.88m2.268-2.268 4.138 3.448m0 0a9.027 9.027 0 0 1-1.306 1.652c-.51.51-1.064.944-1.652 1.306m0 0-3.448-4.138m3.448 4.138a9.014 9.014 0 0 1-9.424 0m5.976-4.138a3.765 3.765 0 0 1-2.528 0m0 0a3.736 3.736 0 0 1-1.388-.88 3.737 3.737 0 0 1-.88-1.388m2.268 2.268L7.288 19.67m0 0a9.024 9.024 0 0 1-1.652-1.306 9.027 9.027 0 0 1-1.306-1.652m0 0 4.138-3.448M4.33 16.712a9.014 9.014 0 0 1 0-9.424m4.138 5.976a3.765 3.765 0 0 1 0-2.528m0 0c.181-.506.475-.982.88-1.388a3.736 3.736 0 0 1 1.388-.88m-2.268 2.268L4.33 7.288m6.406 1.18L7.288 4.33m0 0a9.024 9.024 0 0 0-1.652 1.306A9.025 9.025 0 0 0 4.33 7.288", multi_tenant=True)
    @menu_item('.ipbx.callcenter.queues', l_('Queues'), icon="cubes", svg="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 0 1 0 3.75H5.625a1.875 1.875 0 0 1 0-3.75Z", multi_tenant=True)
    def index(self):
        return super().index()

    def _populate_form(self, form):
        form.extensions[0].exten.choices = self._build_set_choices_exten(
            form.extensions[0]
        )
        form.extensions[0].context.choices = self._build_set_choices_context(
            form.extensions[0]
        )
        form.music_on_hold.choices = self._build_set_choices_moh(form.music_on_hold)
        form.schedules[0].form.id.choices = self._build_set_choices_schedule(
            form.schedules[0]
        )
        form.members.agent_ids.choices = self._build_set_choices_agents(
            form.members.agents
        )
        form.members.user_ids.choices = self._build_set_choices_users(
            form.members.users
        )
        return form

    def _build_set_choices_agents(self, agents):
        return [(agent.form.id.data, agent.form.number.data) for agent in agents]

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            if user.lastname.data:
                text = f'{user.firstname.data} {user.lastname.data}'
            else:
                text = user.firstname.data
            results.append((user.uuid.data, text))
        return results

    def _build_set_choices_exten(self, extension):
        if not extension.exten.data or extension.exten.data == 'None':
            return []
        return [(extension.exten.data, extension.exten.data)]

    def _build_set_choices_context(self, extension):
        if not extension.context.data or extension.context.data == 'None':
            context = self.service.get_first_internal_context()
        else:
            context = self.service.get_context(extension.context.data)

        if context:
            return [(context['name'], context['label'])]

        return [(extension.context.data, extension.context.data)]

    def _build_set_choices_moh(self, moh):
        if not moh.data or moh.data == 'None':
            return []
        moh_object = self.service.get_music_on_hold(moh.data)
        if moh_object is None:
            return []
        moh_label = moh_object['label']
        return [(moh.data, f"{moh_label} ({moh.data})")]

    def _build_set_choices_schedule(self, schedule):
        if not schedule.form.id.data or schedule.form.id.data == 'None':
            return []
        return [(schedule.form.id.data, schedule.form.name.data)]

    def _map_resources_to_form(self, resource):
        resource['options'] = self._build_options(resource['options'])
        resource['members']['agent_ids'] = [
            agent['id'] for agent in resource['members']['agents']
        ]
        resource['members']['user_ids'] = [
            user['uuid'] for user in resource['members']['users']
        ]
        resource['fallbacks'] = self.service.get_fallbacks(resource['id'])
        form = self.form(data=resource)
        return form

    def _build_options(self, options):
        result = []
        for option in options:
            result.append({'option_key': option[0], 'option_value': option[1]})

        return result

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['options'] = self._map_form_to_resource_options(form, resource)
        resource['agents'] = [
            {'id': agent_id} for agent_id in resource['members']['agent_ids']
        ]
        resource['users'] = [
            {'id': user_id} for user_id in resource['members']['user_ids']
        ]
        resource['music_on_hold'] = self._convert_empty_string_to_none(
            form.music_on_hold.data
        )

        return resource

    def _map_form_to_resource_options(self, form, resource):
        options = []
        for option in resource['options']:
            options.append([option['option_key'], option['option_value']])

        return options

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('queue', {}))
        form.extensions[0].populate_errors(resources.get('extension', {}))
        return form


class QueueDestinationView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        queues = self.service.list(**params)
        results = [
            {'id': queue['id'], 'text': queue['name']} for queue in queues['items']
        ]
        return jsonify(build_select2_response(results, queues['total'], params))
