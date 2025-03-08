# Copyright 2023 Accent Communications

from flask import flash, jsonify, render_template, request
from flask_babel import gettext as _
from flask_babel import lazy_gettext as l_
from flask_classful import route
from requests.exceptions import HTTPError

from accent_ui.helpers.classful import LoginRequiredView
from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.view import BaseIPBXHelperView

from .form import ExtensionFeaturesForm, ExtensionForm

MAX_POSSIBILITIES = 1000


class ExtensionView(BaseIPBXHelperView):
    form = ExtensionForm
    resource = 'extension'

    @menu_item(
        '.ipbx.advanced', l_('Advanced'), order=999, icon="gears", svg="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28ZM15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z", multi_tenant=True
    )
    @menu_item(
        '.ipbx.advanced.extensions',
        l_('Extensions'),
        order=1,
        icon="tty",
        svg="M6 13.5V3.75m0 9.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 3.75V16.5m12-3V3.75m0 9.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 3.75V16.5m-6-9V3.75m0 3.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 9.75V10.5",
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _populate_form(self, form):
        form.context.choices = self._build_set_choices_context(form)
        return form

    def _build_set_choices_context(self, extension):
        if not extension.context.data or extension.context.data == 'None':
            return []
        return [(extension.context.data, extension.context.data)]


class ExtensionFeaturesView(BaseIPBXHelperView):
    form = ExtensionFeaturesForm
    resource = 'extension'

    @menu_item(
        '.ipbx.global_settings.extensions_features',
        l_('Extensions Features'),
        order=2,
        icon="fax",
        svg="M6.72 13.829c-.24.03-.48.062-.72.096m.72-.096a42.415 42.415 0 0 1 10.56 0m-10.56 0L6.34 18m10.94-4.171c.24.03.48.062.72.096m-.72-.096L17.66 18m0 0 .229 2.523a1.125 1.125 0 0 1-1.12 1.227H7.231c-.662 0-1.18-.568-1.12-1.227L6.34 18m11.318 0h1.091A2.25 2.25 0 0 0 21 15.75V9.456c0-1.081-.768-2.015-1.837-2.175a48.055 48.055 0 0 0-1.913-.247M6.34 18H5.25A2.25 2.25 0 0 1 3 15.75V9.456c0-1.081.768-2.015 1.837-2.175a48.041 48.041 0 0 1 1.913-.247m10.5 0a48.536 48.536 0 0 0-10.5 0m10.5 0V3.375c0-.621-.504-1.125-1.125-1.125h-8.25c-.621 0-1.125.504-1.125 1.125v3.659M18 10.5h.008v.008H18V10.5Zm-3 0h.008v.008H15V10.5Z",
    )
    def index(self):
        resource = {}
        try:
            resource['extensions'] = self.service.list()['items']
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        return render_template(
            self._get_template('edit_features'), form=self.form(data=resource)
        )

    @route('/put', methods=['POST'])
    def put(self):
        form = self.form()
        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self._index(form)

        resources = form.to_dict()
        try:
            self.service.update_extension_features(resources['extensions'])
        except HTTPError as error:
            self._flash_http_error(error)
            return self._index()

        flash(_('Extensions features has been updated'), 'success')
        return self._redirect_for('index')


class ExtensionListingView(LoginRequiredView):
    def list_available_exten_incall(self):
        return self._list_available_exten(context_range='incall_ranges')

    def list_available_exten_group(self):
        return self._list_available_exten(context_range='group_ranges')

    def list_available_exten_user(self):
        return self._list_available_exten(context_range='user_ranges')

    def list_available_exten_queue(self):
        return self._list_available_exten(context_range='queue_ranges')

    def list_available_exten_conference(self):
        return self._list_available_exten(context_range='conference_room_ranges')

    def _list_available_exten(self, context_range):
        search = request.args.get('term') or ''
        context = request.args.get('context')
        if not context:
            return jsonify({'results': []})

        context = self.service.get_context(context)
        if not context:
            return jsonify({'results': []})

        all_extens = set()
        for ressource_range in context[context_range]:
            try:
                start = int(ressource_range['start'])
                end = int(ressource_range['end']) + 1
            except ValueError:
                continue

            if end - start > MAX_POSSIBILITIES:
                end = start + MAX_POSSIBILITIES

            # TODO benchmark to improve this
            for v in range(start, end):
                if not search or search in str(v):
                    if context_range == 'incall_ranges':
                        all_extens.add(str(v).zfill(ressource_range['did_length']))
                    else:
                        all_extens.add(str(v))

        if not all_extens:
            return jsonify({'results': []})

        used_extens = set()
        for extension in self.service.list(search=search, context=context['name'])[
            'items'
        ]:
            if search and search not in extension['exten']:
                continue

            used_extens.add(extension['exten'])

        valid_extens = all_extens - used_extens
        valid_extens = sorted(valid_extens)

        results = [{'id': exten, 'text': exten} for exten in valid_extens]
        return jsonify({'results': results})
