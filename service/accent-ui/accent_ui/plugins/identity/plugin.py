# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import (
    GroupService,
    IdentityService,
    LDAPService,
    PolicyService,
    TenantService,
)
from .view import (
    GroupListingView,
    GroupView,
    IdentityListingView,
    IdentityView,
    LDAPConfigView,
    PolicyListingView,
    PolicyView,
    TenantListingView,
    TenantView,
)

identity = create_blueprint('identity', __name__)
identity_group = create_blueprint('identity_group', __name__)
tenant = create_blueprint('tenant', __name__)
ldap_config = create_blueprint('ldap', __name__)
policy = create_blueprint('policy', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        IdentityView.service = IdentityService(clients['accent_auth'])
        IdentityView.register(identity, route_base='/identities')
        register_flaskview(identity, IdentityView)

        IdentityListingView.service = IdentityService(clients['accent_auth'])
        IdentityListingView.register(identity, route_base='/identities_listing')

        register_listing_url('identity', 'identity.IdentityListingView:list_json')

        GroupView.service = GroupService(clients['accent_auth'])
        GroupView.register(identity_group, route_base='/identity_groups')
        register_flaskview(identity_group, GroupView)

        GroupListingView.service = GroupService(clients['accent_auth'])
        GroupListingView.register(identity_group, route_base='/identity_groups_listing')

        register_listing_url(
            'identity_group', 'identity_group.GroupListingView:list_json'
        )

        PolicyView.service = PolicyService(clients['accent_auth'])
        PolicyView.register(policy, route_base='/policies')

        TenantView.service = TenantService(clients['accent_auth'])
        TenantView.register(tenant, route_base='/tenants')
        register_flaskview(tenant, TenantView)

        TenantListingView.service = TenantService(clients['accent_auth'])
        TenantListingView.register(tenant, route_base='/tenants_listing')

        register_listing_url('tenant', 'tenant.TenantListingView:list_json')

        register_flaskview(policy, PolicyView)

        PolicyListingView.service = PolicyService(clients['accent_auth'])
        PolicyListingView.register(policy, route_base='/policies_listing')

        register_listing_url('policy', 'policy.PolicyListingView:list_json')

        LDAPConfigView.service = LDAPService(clients['accent_auth'])
        LDAPConfigView.register(ldap_config, route_base='/ldap_config')
        register_flaskview(ldap_config, LDAPConfigView)

        core.register_blueprint(identity)
        core.register_blueprint(identity_group)
        core.register_blueprint(tenant)
        core.register_blueprint(ldap_config)
        core.register_blueprint(policy)
