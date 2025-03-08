# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_

from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.view import BaseIPBXHelperView

from .form import PagingForm


class PagingView(BaseIPBXHelperView):
    form = PagingForm
    resource = 'paging'

    @menu_item(
        '.ipbx.services.pagings', l_('Pagings'), icon="bullhorn", svg="M10.34 15.84c-.688-.06-1.386-.09-2.09-.09H7.5a4.5 4.5 0 1 1 0-9h.75c.704 0 1.402-.03 2.09-.09m0 9.18c.253.962.584 1.892.985 2.783.247.55.06 1.21-.463 1.511l-.657.38c-.551.318-1.26.117-1.527-.461a20.845 20.845 0 0 1-1.44-4.282m3.102.069a18.03 18.03 0 0 1-.59-4.59c0-1.586.205-3.124.59-4.59m0 9.18a23.848 23.848 0 0 1 8.835 2.535M10.34 6.66a23.847 23.847 0 0 0 8.835-2.535m0 0A23.74 23.74 0 0 0 18.795 3m.38 1.125a23.91 23.91 0 0 1 1.014 5.395m-1.014 8.855c-.118.38-.245.754-.38 1.125m.38-1.125a23.91 23.91 0 0 0 1.014-5.395m0-3.46c.495.413.811 1.035.811 1.73 0 .695-.316 1.317-.811 1.73m0-3.46a24.347 24.347 0 0 1 0 3.46", multi_tenant=True
    )
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        members = [user['uuid'] for user in resource['members']['users']]
        callers = [user['uuid'] for user in resource['callers']['users']]
        resource['members']['user_uuids'] = members
        resource['callers']['user_uuids'] = callers
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.members.user_uuids.choices = self._build_set_choices_users(
            form.members.users
        )
        form.callers.user_uuids.choices = self._build_set_choices_users(
            form.callers.users
        )
        return form

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            if user.lastname.data:
                text = f'{user.firstname.data} {user.lastname.data}'
            else:
                text = user.firstname.data
            results.append((user.uuid.data, text))
        return results

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['members']['users'] = [
            {'uuid': user_uuid} for user_uuid in form.members.user_uuids.data
        ]
        resource['callers']['users'] = [
            {'uuid': user_uuid} for user_uuid in form.callers.user_uuids.data
        ]
        return resource

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('paging', {}))
        return form
