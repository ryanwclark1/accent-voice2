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

from .form import OutcallForm


class OutcallView(BaseIPBXHelperView):
    form = OutcallForm
    resource = 'outcall'

    @menu_item(
        '.ipbx.call_management.outcalls',
        l_('Outcalls'),
        order=2,
        icon="long-arrow-left",
        svg="M20.25 3.75v4.5m0-4.5h-4.5m4.5 0-6 6m3 12c-8.284 0-15-6.716-15-15V4.5A2.25 2.25 0 0 1 4.5 2.25h1.372c.516 0 .966.351 1.091.852l1.106 4.423c.11.44-.054.902-.417 1.173l-1.293.97a1.062 1.062 0 0 0-.38 1.21 12.035 12.035 0 0 0 7.143 7.143c.441.162.928-.004 1.21-.38l.97-1.293a1.125 1.125 0 0 1 1.173-.417l4.423 1.106c.5.125.852.575.852 1.091V19.5a2.25 2.25 0 0 1-2.25 2.25h-2.25Z",
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        trunks_ids = [trunk['id'] for trunk in resource['trunks']]
        for extension in resource['extensions']:
            extension['prefix_'] = extension['prefix']
            del extension['prefix']
        resource['call_permission_ids'] = [
            call_permission['id'] for call_permission in resource['call_permissions']
        ]
        form = self.form(data=resource, trunks_ids=trunks_ids)
        return form

    def _populate_form(self, form):
        form.trunks_ids.choices = self._build_set_choices_trunks(form.trunks)
        for form_extension in form.extensions:
            form_extension.context.choices = self._build_set_choices_context(
                form_extension
            )
        form.schedules[0].form.id.choices = self._build_set_choices_schedule(
            form.schedules[0]
        )
        form.call_permission_ids.choices = self._build_set_choices_callpermissions(
            form.call_permissions
        )
        return form

    def _build_set_choices_context(self, extension):
        if not extension.context.data or extension.context.data == 'None':
            context = self.service.get_first_outcall_context()
        else:
            context = self.service.get_context(extension.context.data)

        if context:
            return [(context['name'], context['label'])]

        return [(extension.context.data, extension.context.data)]

    def _build_set_choices_trunks(self, trunks):
        results = []
        for trunk in trunks:
            if not trunk.form.id.data or trunk.form.name.data == 'None':
                results.append((trunk.form.id.data, trunk.form.name.data))
            else:
                trunk_data = self.service.get_trunk(trunk.form.id.data)
                if trunk_data['endpoint_sip']:
                    results.append(
                        (
                            trunk_data['id'],
                            trunk_data['endpoint_sip']['label'] + ' (sip)',
                        )
                    )
                elif trunk_data['endpoint_custom']:
                    results.append(
                        (
                            trunk_data['id'],
                            trunk_data['endpoint_custom']['interface'] + ' (cus)',
                        )
                    )
                elif trunk_data['endpoint_iax']:
                    results.append(
                        (
                            trunk_data['id'],
                            trunk_data['endpoint_iax']['name'] + ' (iax)',
                        )
                    )
        return results

    def _build_set_choices_schedule(self, schedule):
        if not schedule.form.id.data or schedule.form.id.data == 'None':
            return []
        return [(schedule.form.id.data, schedule.form.name.data)]

    def _build_set_choices_callpermissions(self, call_permissions):
        return [
            (call_permission.form.id.data, call_permission.form.name.data)
            for call_permission in call_permissions
        ]

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        if 'trunks_ids' in resource:
            resource['trunks'] = [
                {'id': int(trunk_id)} for trunk_id in resource['trunks_ids']
            ]
        else:
            resource['trunks'] = []
        for extension in resource['extensions']:
            if extension.get('id'):
                extension['id'] = int(extension['id'])
            extension['prefix'] = extension['prefix_']
            del extension['prefix_']
        resource['call_permissions'] = [
            {'id': call_permission_id}
            for call_permission_id in form.call_permission_ids.data
        ]
        return resource

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('outcall', {}))
        form.populate_errors(resources.get('extensions', {}))
        return form


class OutcallDestinationView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        outcalls = self.service.list(**params)
        results = [
            {'id': outcall['id'], 'text': outcall['name']}
            for outcall in outcalls['items']
        ]
        return jsonify(build_select2_response(results, outcalls['total'], params))
