# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_

from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.view import BaseIPBXHelperView

from .form import IncallForm


class IncallView(BaseIPBXHelperView):
    form = IncallForm
    resource = 'incall'

    @menu_item(
        '.ipbx.call_management',
        l_('Call Management'),
        order=2,
        icon="phone",
        svg="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z",
        multi_tenant=True,
    )
    @menu_item(
        '.ipbx.call_management.incalls',
        l_('Incalls'),
        order=1,
        icon="long-arrow-right",
        svg="M14.25 9.75v-4.5m0 4.5h4.5m-4.5 0 6-6m-3 18c-8.284 0-15-6.716-15-15V4.5A2.25 2.25 0 0 1 4.5 2.25h1.372c.516 0 .966.351 1.091.852l1.106 4.423c.11.44-.054.902-.417 1.173l-1.293.97a1.062 1.062 0 0 0-.38 1.21 12.035 12.035 0 0 0 7.143 7.143c.441.162.928-.004 1.21-.38l.97-1.293a1.125 1.125 0 0 1 1.173-.417l4.423 1.106c.5.125.852.575.852 1.091V19.5a2.25 2.25 0 0 1-2.25 2.25h-2.25Z",
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _populate_form(self, form):
        form.extensions[0].exten.choices = self._build_set_choices_exten(
            form.extensions[0]
        )
        form.extensions[0].context.choices = self._build_set_choices_context(
            form.extensions[0]
        )
        form.schedules[0].form.id.choices = self._build_set_choices_schedule(
            form.schedules[0]
        )
        sounds = self.service.list_sound()
        form.greeting_sound.choices = self._build_set_choices_sound(sounds)
        return form

    def _build_set_choices_exten(self, extension):
        if not extension.exten.data or extension.exten.data == 'None':
            return []
        return [(extension.exten.data, extension.exten.data)]

    def _build_set_choices_context(self, extension):
        if not extension.context.data or extension.context.data == 'None':
            context = self.service.get_first_incall_context()
        else:
            context = self.service.get_context(extension.context.data)

        if context:
            return [(context['name'], context['label'])]

        return [(extension.context.data, extension.context.data)]

    def _build_set_choices_schedule(self, schedule):
        if not schedule.form.id.data or schedule.form.id.data == 'None':
            return []
        return [(schedule.form.id.data, schedule.form.name.data)]

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
        form.populate_errors(resources.get('incall', {}))
        form.extensions[0].populate_errors(resources.get('extension', {}))
        return form
