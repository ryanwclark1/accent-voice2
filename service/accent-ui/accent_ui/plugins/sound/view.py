# Copyright 2023 Accent Communications

import cgi
from io import BytesIO

from flask import flash, jsonify, redirect, render_template, request, send_file, url_for
from flask_babel import gettext as _
from flask_babel import lazy_gettext as l_
from flask_classful import route
from requests.exceptions import HTTPError

from accent_ui.helpers.classful import LoginRequiredView
from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.view import BaseIPBXHelperView

from .form import SoundFilenameForm, SoundForm


class SoundView(BaseIPBXHelperView):
    form = SoundForm
    resource = 'sound'

    @menu_item(
        '.ipbx.sound_greeting.sound',
        l_('Sound Files'),
        icon="file-sound-o",
        svg="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z",
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

        sounds = []
        for sound in resource_list['items']:
            if sound['name'] == 'system':
                continue
            sound['id'] = sound['name']
            sounds.append(sound)

        resource_list['items'] = sounds

        return render_template(
            self._get_template('list'),
            form=self.form(),
            resource_list=resource_list,
            current_breadcrumbs=self._get_current_breadcrumbs(),
            listing_urls=self.listing_urls,
        )

    @route('/delete/<tenant_uuid>/<category>')
    def delete(self, tenant_uuid, category):
        try:
            self.service.delete(tenant_uuid, category)
            flash(
                _(
                    '%(resource)s: Resource %(category)s has been deleted',
                    resource=self.resource,
                    category=category,
                ),
                'success',
            )
        except HTTPError as error:
            self._flash_http_error(error)

        return self._redirect_for('index')

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('sound', {}))
        return form


class SoundFileView(BaseIPBXHelperView):
    form = SoundFilenameForm
    resource = 'sound'

    @menu_item(
        '.ipbx.global_settings.sound_system',
        l_('Sound Files System'),
        order=2,
        icon="file-sound-o",
        svg="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z"
    )
    def sound_files_system(self):
        sound = self._get_sound_by_category(tenant_uuid=None, category='system')
        return render_template(
            self._get_template('list_system_files'),
            form=self.form(),
            sound=sound,
            current_breadcrumbs=self._get_current_breadcrumbs(),
            listing_urls=self.listing_urls,
        )

    @route('/list_files/<tenant_uuid>/<category>')
    def list_files(self, tenant_uuid, category):
        sound = self._get_sound_by_category(tenant_uuid, category)
        return render_template(
            self._get_template('list_files'),
            form=SoundFilenameForm(),
            sound=sound,
            current_breadcrumbs=self._get_current_breadcrumbs(),
            listing_urls=self.listing_urls,
        )

    def _get_sound_by_category(self, tenant_uuid, category):
        try:
            sound = self.service.get(tenant_uuid, category)
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('admin.Admin:get'))

        return sound

    def download_sound_filename(self, tenant_uuid, category, filename):
        response = self.service.download_sound_filename(
            tenant_uuid,
            category,
            filename,
            format_=request.args.get('format'),
            language=request.args.get('language'),
        )
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            _, params = cgi.parse_header(content_disposition)
            if params:
                filename = params['filename']

        return send_file(
            BytesIO(response.content),
            attachment_filename=filename,
            as_attachment=True,
            mimetype=response.headers.get('content-type'),
        )

    def download_system_sound_filename(self, filename):
        return self.download_sound_filename(
            tenant_uuid=None, category='system', filename=filename
        )

    @route('/upload_sound_filename/<tenant_uuid>/<category>', methods=['POST'])
    def upload_sound_filename(self, tenant_uuid, category):
        if 'name' not in request.files:
            flash(l_('[upload] Upload attempt with no file'), 'error')
            return redirect(
                url_for(
                    '.SoundFileView:list_files',
                    tenant_uuid=tenant_uuid,
                    category=category,
                )
            )

        file_ = request.files.get('name')

        form = self.form()
        resources = self._map_form_to_resources_post(form)
        del resources['name']

        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return redirect(
                url_for(
                    '.SoundFileView:list_files',
                    tenant_uuid=tenant_uuid,
                    category=category,
                )
            )

        try:
            self.service.upload_sound_filename(
                tenant_uuid, category, file_.filename, file_.read(), **resources
            )
        except HTTPError as error:
            self._flash_http_error(error)

        return redirect(
            url_for(
                '.SoundFileView:list_files', tenant_uuid=tenant_uuid, category=category
            )
        )

    def delete_sound_filename(self, tenant_uuid, category, filename):
        self.service.delete_sound_filename(
            tenant_uuid,
            category,
            filename,
            format_=request.args.get('format'),
            language=request.args.get('language'),
        )
        return redirect(
            url_for(
                '.SoundFileView:list_files', tenant_uuid=tenant_uuid, category=category
            )
        )

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('sound', {}))
        return form


class SoundListingView(LoginRequiredView):
    def list_json(self):
        sounds = self.service.list()
        results = []
        for sound in sounds['items']:
            for file_ in sound['files']:
                for format_ in file_['formats']:
                    format_label = (
                        f' [{format_["format"]}]' if format_['format'] else ''
                    )
                    language_label = (
                        f' ({format_["language"]})' if format_['language'] else ''
                    )
                    results.append(
                        {
                            'text': f'{file_["name"]}{format_label}{language_label}',
                            'id': file_['name']
                            if sound['name'] == 'system'
                            else format_['path'],
                        }
                    )

        return jsonify({'results': results})
