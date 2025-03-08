# Copyright 2023 Accent Communications

import pprint

from flask import redirect, render_template, url_for
from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError

from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.view import BaseIPBXHelperView

from .form import WebhookFormHTTP


class WebhookView(BaseIPBXHelperView):
    form = WebhookFormHTTP
    resource = 'webhook'
    raw_events = []

    @menu_item(
        '.ipbx.services.webhooks', l_('Webhooks'), icon="globe", svg="m6.115 5.19.319 1.913A6 6 0 0 0 8.11 10.36L9.75 12l-.387.775c-.217.433-.132.956.21 1.298l1.348 1.348c.21.21.329.497.329.795v1.089c0 .426.24.815.622 1.006l.153.076c.433.217.956.132 1.298-.21l.723-.723a8.7 8.7 0 0 0 2.288-4.042 1.087 1.087 0 0 0-.358-1.099l-1.33-1.108c-.251-.21-.582-.299-.905-.245l-1.17.195a1.125 1.125 0 0 1-.98-.314l-.295-.295a1.125 1.125 0 0 1 0-1.591l.13-.132a1.125 1.125 0 0 1 1.3-.21l.603.302a.809.809 0 0 0 1.086-1.086L14.25 7.5l1.256-.837a4.5 4.5 0 0 0 1.528-1.732l.146-.292M6.115 5.19A9 9 0 1 0 17.18 4.64M6.115 5.19A8.965 8.965 0 0 1 12 3c1.929 0 3.716.607 5.18 1.64", multi_tenant=True
    )
    def index(self):
        return super().index()

    def get_logs(self, id):
        try:
            resource_list = self.service.get_logs(id)
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('index.IndexView:index'))
        for item in resource_list["items"]:
            item["detail"] = pprint.pformat(item["detail"], width=160, indent=2)
            item["event"] = pprint.pformat(item["event"], width=80, indent=2)
        return render_template(
            self._get_template('logs'),
            resource=self.service.get(id),
            resource_list=resource_list,
            current_breadcrumbs=self._get_current_breadcrumbs(),
            listing_urls=self.listing_urls,
        )

    def _populate_form(self, form):
        users_by_id = {
            user['uuid']: str(user['firstname']) + ' ' + str(user['lastname'])
            for user in self.service.list_users()['items']
        }

        form.events.choices = [(event, event) for event in self.raw_events]
        form.services.choices = self._build_choices_services()
        form.user_uuid.choices = self._build_setted_choices_users(
            form.events_user_uuid, users_by_id
        )
        return form

    def _map_resources_to_form(self, resource):
        self.raw_events = resource['events']

        resource['events'] = resource.get('events')
        resource['services'] = resource.get('service')

        resource['url'] = resource['config'].get('url')
        resource['body'] = resource['config'].get('body')
        resource['verify_certificate'] = resource['config'].get('verify_certificate')
        resource['method'] = resource['config'].get('method')
        resource['content_type'] = resource['config'].get('content_type')

        form = self.form(data=resource)
        return form

    def _build_choices_services(self):
        services = self.service.list_services()
        services_list = [((''), ('Choose a service'))]
        for service in services['services']:
            services_list.append((service, service))
        return services_list

    def _build_setted_choices_users(self, user_uuid, users_by_id):
        if not user_uuid.data or user_uuid.data == 'None':
            return []
        return [(user_uuid.data, users_by_id[user_uuid.data])]
