# Copyright 2023 Accent Communications

from flask import jsonify, request
from flask_babel import lazy_gettext as l_

from accent_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params,
)
from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.view import BaseIPBXHelperView, NewHelperViewMixin

from .form import EndpointSIPForm

SECTIONS = [
    'aor_section_options',
    'auth_section_options',
    'endpoint_section_options',
    'identify_section_options',
    'registration_section_options',
    'registration_outbound_auth_section_options',
    'outbound_auth_section_options',
]

EXCLUDE_CHOICE_SECTIONS = [
    'identify_section_options',
    'registration_section_options',
]


class EndpointSIPTemplateView(NewHelperViewMixin, BaseIPBXHelperView):
    form = EndpointSIPForm
    resource = l_('SIP Template')

    @menu_item(
        '.ipbx.advanced.sip_templates',
        l_('SIP Templates'),
        icon="compress",
        svg="M21 11.25v8.25a1.5 1.5 0 0 1-1.5 1.5H5.25a1.5 1.5 0 0 1-1.5-1.5v-8.25M12 4.875A2.625 2.625 0 1 0 9.375 7.5H12m0-2.625V7.5m0-2.625A2.625 2.625 0 1 1 14.625 7.5H12m0 0V21m-8.625-9.75h18c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125h-18c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z",
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _populate_form(self, form):
        form.transport.form.uuid.choices = self._build_set_choices_transport(form)
        form.template_uuids.choices = self._build_set_choices_templates(form.templates)
        return form

    def _build_set_choices_transport(self, template):
        transport_uuid = template.transport.form.uuid.data
        if not transport_uuid or transport_uuid == 'None':
            return []
        transport = self.service.get_transport(transport_uuid)
        return [(transport['uuid'], transport['name'])]

    def _build_set_choices_templates(self, templates):
        results = []
        for template in templates:
            template = self.service.get_sip_template(template.uuid.data)
            results.append((template['uuid'], template['label']))
        return results

    def _map_resources_to_form(self, resource):
        choices = []
        for section in SECTIONS:
            for key, _ in resource[section]:
                choices.append((key, key))

            resource[section] = self._build_options(resource[section])

        resource['template_uuids'] = [
            template['uuid'] for template in resource['templates']
        ]

        form = self.form(data=resource)

        for section in SECTIONS:
            if section in EXCLUDE_CHOICE_SECTIONS:
                continue

            for option in getattr(form, section):
                option.option_key.choices = choices

        return form

    def _build_options(self, options):
        return [
            {'option_key': option_key, 'option_value': option_value}
            for option_key, option_value in options
        ]

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        for section in SECTIONS:
            resource[section] = self._map_options_to_resource(resource[section])

        if not resource['transport'].get('uuid'):
            resource['transport'] = None

        resource['templates'] = [
            {'uuid': template_uuid} for template_uuid in form.template_uuids.data
        ]

        return resource

    def _map_options_to_resource(self, options):
        return [[option['option_key'], option['option_value']] for option in options]


class SIPTemplateDestinationView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        templates = self.service.list(**params)
        results = [{'id': t['uuid'], 'text': t['label']} for t in templates['items']]
        return jsonify(build_select2_response(results, templates['total'], params))
