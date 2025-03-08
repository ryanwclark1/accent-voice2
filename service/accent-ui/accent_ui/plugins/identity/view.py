# Copyright 2023 Accent Communications

from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_babel import lazy_gettext as l_
from flask_classful import route
from requests.exceptions import HTTPError

from accent_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params,
)
from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.tenant import refresh_tenants
from accent_ui.helpers.view import BaseIPBXHelperView

from .form import GroupForm, IdentityForm, LDAPForm, PolicyForm, TenantForm


class IdentityView(BaseIPBXHelperView):
    form = IdentityForm
    resource = 'identity'

    @menu_item(
        '.ipbx.identity', l_('Credentials'), icon="user-secret", svg="M9.348 14.652a3.75 3.75 0 0 1 0-5.304m5.304 0a3.75 3.75 0 0 1 0 5.304m-7.425 2.121a6.75 6.75 0 0 1 0-9.546m9.546 0a6.75 6.75 0 0 1 0 9.546M5.106 18.894c-3.808-3.807-3.808-9.98 0-13.788m13.788 0c3.808 3.807 3.808 9.98 0 13.788M12 12h.008v.008H12V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z", multi_tenant=True
    )
    @menu_item(
        '.ipbx.identity.identities',
        l_('Identities'),
        order=1,
        icon="user",
        svg='M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z',
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        resource['members']['group_uuids'] = [
            group['uuid'] for group in resource['members']['groups']
        ]
        resource['members']['policy_uuids'] = [
            policy['uuid'] for policy in resource['members']['policies']
        ]
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.members.group_uuids.choices = self._build_set_choices_groups(
            form.members.groups
        )
        form.members.policy_uuids.choices = self._build_set_choices_policies(
            form.members.policies
        )
        return form

    def _build_set_choices_groups(self, groups):
        results = []
        for group in groups:
            results.append((group.form.uuid.data, group.form.name.data))
        return results

    def _build_set_choices_policies(self, policies):
        results = []
        for policy in policies:
            results.append((policy.form.uuid.data, policy.form.name.data))
        return results

    def _map_form_to_resources(self, form, form_id=None):
        resource = form.to_dict()
        if form_id:
            resource['uuid'] = form_id
        resource['members']['groups'] = [
            {'uuid': group_uuid} for group_uuid in form.members.group_uuids.data
        ]
        resource['members']['policies'] = [
            {'uuid': policy_uuid} for policy_uuid in form.members.policy_uuids.data
        ]
        return resource


class IdentityListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        identities = self.service.list(**params)
        results = [
            {'id': identity['uuid'], 'text': identity['username']}
            for identity in identities['items']
        ]
        return jsonify(build_select2_response(results, identities['total'], params))


class GroupView(BaseIPBXHelperView):
    form = GroupForm
    resource = 'identity_group'

    @menu_item(
        '.ipbx.identity.groups', l_('Groups'), order=2, icon="users", svg='M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z', multi_tenant=True
    )
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        resource['members']['user_uuids'] = [
            user['uuid'] for user in resource['members']['users']
        ]
        resource['members']['policy_uuids'] = [
            policy['uuid'] for policy in resource['members']['policies']
        ]
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.members.user_uuids.choices = self._build_set_choices_users(
            form.members.users
        )
        form.members.policy_uuids.choices = self._build_set_choices_policies(
            form.members.policies
        )
        return form

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            results.append((user.uuid.data, user.username.data))
        return results

    def _build_set_choices_policies(self, policies):
        results = []
        for policy in policies:
            results.append((policy.form.uuid.data, policy.form.name.data))
        return results

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['members']['users'] = [
            {'uuid': user_uuid} for user_uuid in form.members.user_uuids.data
        ]
        resource['members']['policies'] = [
            {'uuid': policy_uuid} for policy_uuid in form.members.policy_uuids.data
        ]
        return resource


class GroupListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        groups = self.service.list(**params)
        results = [
            {'id': group['uuid'], 'text': group['name']} for group in groups['items']
        ]
        return jsonify(build_select2_response(results, groups['total'], params))


class TenantView(BaseIPBXHelperView):
    form = TenantForm
    resource = 'tenant'

    @menu_item('.ipbx.global_settings.tenants', l_('Tenants'), order=3, icon="building", svg="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21")
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
        )

    def post(self):
        result = super().post()
        refresh_tenants()

        return result

    @route('/put/<id>', methods=['POST'])
    def put(self, id):
        result = super().put(id)
        refresh_tenants()

        return result

    @route('/delete/<id>', methods=['GET'])
    def delete(self, id):
        result = super().delete(id)
        refresh_tenants()

        return result

    def _map_resources_to_form(self, resource):
        resource['members']['user_uuids'] = [
            user['uuid'] for user in resource['members']['users']
        ]
        resource['members']['policy_uuids'] = [
            policy['uuid'] for policy in resource['members']['policies']
        ]
        resource['domains'] = [{'name': name} for name in resource['domain_names']]
        form = self.form(data=resource)
        return form

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        domains = resource.pop('domains')
        resource['domain_names'] = [
            domain['name'] for domain in domains if domain['name']
        ]
        return resource

    def _populate_form(self, form):
        form.members.user_uuids.choices = self._build_set_choices_users(
            form.members.users
        )
        form.members.policy_uuids.choices = self._build_set_choices_policies(
            form.members.policies
        )
        return form

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            results.append((user.uuid.data, user.username.data))
        return results

    def _build_set_choices_policies(self, policies):
        results = []
        for policy in policies:
            results.append((policy.form.uuid.data, policy.form.name.data))
        return results


class TenantListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        tenants = self.service.list(**params)
        results = [
            {'id': tenant['uuid'], 'text': tenant['name']}
            for tenant in tenants['items']
        ]
        return jsonify(build_select2_response(results, tenants['total'], params))


class PolicyView(BaseIPBXHelperView):
    form = PolicyForm
    resource = 'policy'

    @menu_item(
        '.ipbx.identity.policies',
        l_('Policies'),
        order=4,
        icon="lock",
        svg="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z",
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        resource['acl'] = [{'value': access} for access in resource['acl']]
        form = self.form(data=resource)
        return form

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['acl'] = [access['value'] for access in resource['acl']]
        return resource


class PolicyListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        groups = self.service.list(**params)
        results = [
            {'id': group['uuid'], 'text': group['name']} for group in groups['items']
        ]
        return jsonify(build_select2_response(results, groups['total'], params))


class LDAPConfigView(BaseIPBXHelperView):
    form = LDAPForm
    resource = 'ldap'

    @menu_item(
        '.ipbx.identity.ldap', l_('LDAP'), order=5, icon="wrench", svg="M11.42 15.17 17.25 21A2.652 2.652 0 0 0 21 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 1 1-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 0 0 4.486-6.336l-3.276 3.277a3.004 3.004 0 0 1-2.25-2.25l3.276-3.276a4.5 4.5 0 0 0-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437 1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008Z", multi_tenant=True
    )
    def index(self, form=None):
        resource = self.service.get()
        form = form or self.form()
        return render_template(
            self._get_template('index'), form=self.form(data=resource)
        )

    def _map_form_to_resources_post(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['protocol_security'] = self._convert_empty_string_to_none(
            form.protocol_security.data
        )
        return resource

    def post(self):
        form = self.form()
        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self.index(form)

        resource = self._map_form_to_resources_post(form)
        try:
            self.service.update(resource)
        except HTTPError as error:
            self._flash_http_error(error)
            return self.index()

        flash(l_('LDAP config has been updated'), 'success')
        return self._redirect_for('index')

    @route('/delete', methods=['GET'])
    def delete(self):
        try:
            self.service.delete()
            flash(
                l_(
                    '%(resource)s: LDAP configuration has been deleted',
                    resource=self.resource,
                ),
                'success',
            )
        except HTTPError as error:
            self._flash_http_error(error)

        return self._redirect_referrer_or('index')
