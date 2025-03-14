# Copyright 2023 Accent Communications

from flask import jsonify, redirect, render_template, request, url_for
from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError

from accent_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params,
)
from accent_ui.helpers.extension import clean_extension
from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.view import BaseIPBXHelperView

from .form import CallFilterForm, bs_strategy_map


class CallFilterView(BaseIPBXHelperView):
    form = CallFilterForm
    resource = 'call_filter'

    @menu_item(
        '.ipbx.call_management.callfilters',
        l_('BS Filters'),
        icon="filter",
        svg="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z",
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _index(self, form=None):
        try:
            resource_list = self.service.list()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('admin.Admin:get'))

        form = form or self.form()
        form = self._populate_form(form)

        return render_template(
            self._get_template('list'),
            form=form,
            resource_list=resource_list,
            listing_urls=self.listing_urls,
            current_breadcrumbs=self._get_current_breadcrumbs(),
            bs_strategy_map=bs_strategy_map,
        )

    def _map_resources_to_form(self, resource):
        surrogates_user = {}
        surrogates_user['user_uuids'] = [
            user['uuid'] for user in resource['surrogates']['users']
        ]
        surrogates_user['users'] = self._build_surrogates_user(
            resource['surrogates']['users']
        )
        recipients_user = self._build_recipients_user(resource['recipients']['users'])
        fallbacks = self._build_sound(resource['fallbacks'])
        form = self.form(
            data=resource,
            fallbacks=fallbacks,
            surrogates_user=surrogates_user,
            recipients_user=recipients_user,
        )
        return form

    def _build_surrogates_user(self, surrogates_user):
        for surrogate_user in surrogates_user:
            user = self.service.get_user_by_uuid(surrogate_user['uuid'])
            surrogate_user['id'] = user['id']
        return surrogates_user

    def _build_sound(self, fallbacks):
        if (
            not fallbacks['noanswer_destination']
            or fallbacks['noanswer_destination']['type'] != 'sound'
        ):
            return fallbacks
        file_, format_ = self.service.find_sound_by_path(
            fallbacks['noanswer_destination']['filename']
        )
        if file_:
            fallbacks['noanswer_destination']['name'] = file_['name']
            fallbacks['noanswer_destination']['format'] = format_['format']
            fallbacks['noanswer_destination']['language'] = format_['language']
        return fallbacks

    def _build_recipients_user(self, recipients_user):
        for user in recipients_user:
            return user
        return None

    def _populate_form(self, form):
        sounds = self.service.list_sound()
        form.fallbacks.form.noanswer_destination.choices = (
            self._build_set_choices_sound(sounds)
        )
        form.surrogates_user.user_uuids.choices = (
            self._build_set_choices_surrogates_user(form.surrogates_user.users)
        )
        form.recipients_user.uuid.choices = self._build_set_choices_recipient_users(
            [form.recipients_user]
        )
        return form

    def _build_set_choices_recipient_users(self, users):
        results = []
        for user in users:
            if user.firstname.data and user.lastname.data:
                last_name = f' {user.lastname.data}' if user.lastname.data else ''
                text = f'{user.firstname.data}{last_name}'
            elif user.uuid.data:
                user_data = self.service.get_user_by_uuid(user.uuid.data)
                last_name = f' {user_data["lastname"]}' if user_data['lastname'] else ''
                text = f'{user_data["firstname"]}{last_name}'
            else:
                continue
            results.append((user.uuid.data, text))
        return results

    def _build_set_choices_surrogates_user(self, users):
        bsfilter_extension = self.service.get_bsfilter_extension()
        bsfilter_exten = clean_extension(bsfilter_extension['exten'])
        results = []
        for user in users:
            last_name = f' {user.lastname.data}' if user.lastname.data else ''
            bsfilter_label = (
                f' ({bsfilter_exten}{user.member_id.data})' if bsfilter_exten else ''
            )
            text = f'{user.firstname.data}{last_name}{bsfilter_label}'
            results.append((user.uuid.data, text))
        return results

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
        file_format = f' [{format_["format"]}]' if format_['format'] else ''
        language = f' ({format_["language"]})' if format_['language'] else ''
        return f'{file_["name"]}{file_format}{language}'

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['recipients_user'] = [resource['recipients_user']]
        resource['surrogates_user'] = [
            {'uuid': uuid} for uuid in resource['surrogates_user']['user_uuids']
        ]
        return resource


class CallFilterMemberListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        callfilters = self.service.list(**params)
        results = [
            {
                'id': user['member_id'],
                'text': '{}{}'.format(
                    user['firstname'],
                    f" {user['lastname']}" if user['lastname'] else '',
                ),
            }
            for callfilter in callfilters['items']
            for user in callfilter['surrogates']['users']
        ]
        return jsonify(build_select2_response(results, callfilters['total'], params))
