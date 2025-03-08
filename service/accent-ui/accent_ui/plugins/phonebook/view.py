# Copyright 2023 Accent Communications

from __future__ import annotations

import logging

from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError

from accent_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params,
    route,
)
from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.view import BaseIPBXHelperView
from accent_ui.plugins.phonebook.service import (
    ContactSelector,
    ManagePhonebookContactsService,
)

from .form import ManagePhonebookForm, PhonebookForm

logger = logging.getLogger(__name__)


class PhonebookView(BaseIPBXHelperView):
    form = PhonebookForm
    resource = 'phonebook'

    @menu_item('.ipbx.phonebooks', l_('Phonebooks'), icon="book", svg="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25", multi_tenant=True)
    @menu_item(
        '.ipbx.phonebooks.config',
        l_('Configuration'),
        order=1,
        icon="wrench",
        svg="M21.75 6.75a4.5 4.5 0 0 1-4.884 4.484c-1.076-.091-2.264.071-2.95.904l-7.152 8.684a2.548 2.548 0 1 1-3.586-3.586l8.684-7.152c.833-.686.995-1.874.904-2.95a4.5 4.5 0 0 1 6.336-4.486l-3.276 3.276a3.004 3.004 0 0 0 2.25 2.25l3.276-3.276c.256.565.398 1.192.398 1.852ZM4.867 19.125h.008v.008h-.008v-.008Z",
        multi_tenant=True,
    )
    def index(self):
        logger.debug('Rendering phonebook index page(args=%s)', request.args)
        return super().index()


class ManagePhonebookView(BaseIPBXHelperView):
    form = ManagePhonebookForm
    resource = 'phonebook'
    settings = 'manage_phonebook'
    service: ManagePhonebookContactsService

    @menu_item(
        '.ipbx.phonebooks.manage',
        l_('Contacts'),
        order=2,
        icon="users",
        svg='M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z',
        multi_tenant=True,
    )
    def index(self, form=None):
        phonebook_uuid = request.args.get('phonebook_uuid')
        try:
            phonebook_list = self.service.list_phonebook()
            if len(phonebook_list) < 1:
                flash(l_('Please add phonebook before adding contacts!'), 'error')
                return redirect(url_for('accent_engine.phonebook.PhonebookView:index'))
            default_phonebook = phonebook_list[0]
            phonebook_uuid = phonebook_uuid or default_phonebook.get('uuid')
            resource_list = self.service.list(phonebook_uuid=phonebook_uuid)
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('accent_engine.phonebook.PhonebookView:index'))

        form = form or self._map_resources_to_form(dict(phonebook_uuid=phonebook_uuid))
        form = self._populate_form(form)

        kwargs = {
            'form': form,
            'resource_list': resource_list,
            'phonebook_uuid': phonebook_uuid,
            'phonebook_list': phonebook_list,
        }
        if self.listing_urls:
            kwargs['listing_urls'] = self.listing_urls
        return render_template(self._get_template(self.settings), **kwargs)

    def post(self):
        form = self.form()
        resources = self._map_form_to_resources_post(form)

        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self._new(form)

        try:
            self.service.create(resources)
        except HTTPError as error:
            form = self._fill_form_error(form, error)
            self._flash_http_error(error)
            return self._new(form)

        flash(
            l_('%(resource)s: Resource has been created', resource=self.resource),
            'success',
        )
        return self._redirect_referrer_or('index')

    @route('/delete/<phonebook_uuid>/<id>', methods=['GET'])
    def delete(self, phonebook_uuid, id):
        try:
            self.service.delete(
                ContactSelector(phonebook_uuid=phonebook_uuid, contact_id=id)
            )
            flash(
                l_(
                    '%(resource)s: Resource %(id)s has been deleted',
                    resource=self.resource,
                    id=id,
                ),
                'success',
            )
        except HTTPError as error:
            self._flash_http_error(error)

        return self._redirect_referrer_or('index')

    def get(self, id):
        return self._get(id, phonebook_uuid=request.args.get('phonebook_uuid'))

    def _map_form_to_resources(
        self, form: ManagePhonebookForm, form_id: str | None = None
    ):
        data = form.to_dict()
        if form_id:
            data['id'] = form_id
        return data

    def _get(
        self,
        id: str,
        form: ManagePhonebookForm | None = None,
        phonebook_uuid: str | None = None,
    ):
        assert (form and form.phonebook_uuid) or phonebook_uuid
        try:
            resource = self.service.get(
                ContactSelector(
                    phonebook_uuid=(
                        (form and str(form.phonebook_uuid)) or phonebook_uuid  # type: ignore[arg-type]
                    ),
                    contact_id=id,
                )
            )
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        form = self._map_resources_to_form(
            dict(resource, phonebook_uuid=phonebook_uuid)
        )
        form = self._populate_form(form)

        return render_template(
            self._get_template('edit_contact'),
            form=form,
            resource=resource,
            current_breadcrumbs=self._get_current_breadcrumbs(),
            listing_urls=self.listing_urls,
        )


class PhonebookDestinationView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        phonebooks = self.service.list(**params)
        results = [
            {'id': phonebook['uuid'], 'text': phonebook['name']}
            for phonebook in phonebooks['items']
        ]
        return jsonify(build_select2_response(results, phonebooks['total'], params))
