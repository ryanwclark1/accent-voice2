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

from .form import IvrForm


class IvrView(NewHelperViewMixin, BaseIPBXHelperView):
    form = IvrForm
    resource = 'ivr'

    @menu_item('.ipbx.services.ivr', l_('IVR'), icon="navicon", svg="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178ZM15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z", multi_tenant=True)
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        self._build_ivr_choices_sound(resource)
        form = self.form(data=resource)
        return form

    def _build_ivr_choices_sound(self, resource):
        for choice in resource['choices']:
            if choice['destination']['type'] != 'sound':
                continue
            file_, format_ = self.service.find_sound_by_path(
                choice['destination']['filename']
            )
            if file_:
                choice['destination']['name'] = file_['name']
                choice['destination']['format'] = format_['format']
                choice['destination']['language'] = format_['language']

    def _populate_form(self, form):
        sounds = self.service.list_sound()
        form.menu_sound.choices = self._build_set_choices_sound(sounds)
        form.invalid_sound.choices = self._build_set_choices_sound(sounds)
        form.greeting_sound.choices = self._build_set_choices_sound(sounds)
        form.abort_sound.choices = self._build_set_choices_sound(sounds)
        return form

    def _build_set_choices_sound(self, sounds):
        results = [('', l_('None'))]
        for sound in sounds['items']:
            for file_ in sound['files']:
                for format_ in file_['formats']:
                    name = (
                        format_['path'] if sound['name'] != 'system' else file_['name']
                    )
                    label = self._prepare_sound_filename_label(file_, format_)
                    results.append((name, label))
        return results

    def _prepare_sound_filename_label(self, file_, format_):
        format_label = f' [{format_["format"]}]' if format_['format'] else ''
        language_label = f' ({format_["language"]})' if format_['language'] else ''
        return f'{file_["name"]}{format_label}{language_label}'

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('ivr', {}))
        return form


class IvrDestinationView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        ivrs = self.service.list(**params)
        results = [{'id': ivr['id'], 'text': ivr['name']} for ivr in ivrs['items']]
        return jsonify(build_select2_response(results, ivrs['total'], params))
