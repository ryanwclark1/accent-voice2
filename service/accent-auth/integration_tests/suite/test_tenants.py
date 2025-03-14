# Copyright 2023 Accent Communications

from uuid import uuid4

from accent_test_helpers import until
from accent_test_helpers.hamcrest.uuid_ import uuid_
from hamcrest import (
    assert_that,
    contains_exactly,
    contains_inanyorder,
    empty,
    equal_to,
    has_entries,
    has_entry,
    has_item,
    is_,
)

from .helpers import base, fixtures
from .helpers.base import ADDRESS_NULL, assert_http_error, assert_no_error
from .helpers.constants import ALL_USERS_POLICY_SLUG, UNKNOWN_UUID

ADDRESS_1 = {
    'line_1': 'Here',
    'city': 'Québec',
    'state': 'Québec',
    'country': 'Canada',
    'zip_code': 'H0H 0H0',
}
PHONE_1 = '555-555-5555'

VALID_DOMAIN_NAMES_1 = ['accentvoice.io', 'shopify.ca']
VALID_DOMAIN_NAMES_2 = ['gmail.com', 'yahoo.com', 'google.ca']
VALID_DOMAIN_NAMES_3 = ['outlook.fr', 'mail.yahoo.fr']


@base.use_asset('base')
class TestTenants(base.APIIntegrationTest):
    @fixtures.http.tenant(
        name='foobar',
        address=ADDRESS_1,
        phone=PHONE_1,
        slug='slug1',
        domain_names=VALID_DOMAIN_NAMES_1,
    )
    @fixtures.http.tenant(
        uuid='6668ca15-6d9e-4000-b2ec-731bc7316767',
        name='foobaz',
        slug='slug2',
        domain_names=VALID_DOMAIN_NAMES_2,
        default_authentication_method='ldap',
    )
    @fixtures.http.tenant(slug='slug3', default_authentication_method='saml')
    def test_post(self, foobar, foobaz, other):
        assert_that(
            other,
            has_entries(
                uuid=uuid_(),
                name=None,
                slug='slug3',
                parent_uuid=self.top_tenant_uuid,
                address=has_entries(**ADDRESS_NULL),
                domain_names=is_(empty()),
                default_authentication_method='saml',
            ),
        )
        assert_that(
            foobaz,
            has_entries(
                uuid='6668ca15-6d9e-4000-b2ec-731bc7316767',
                name='foobaz',
                slug='slug2',
                parent_uuid=self.top_tenant_uuid,
                address=has_entries(**ADDRESS_NULL),
                domain_names=contains_inanyorder(*VALID_DOMAIN_NAMES_2),
                default_authentication_method='ldap',
            ),
        )

        assert_that(
            foobar,
            has_entries(
                uuid=uuid_(),
                name='foobar',
                slug='slug1',
                phone=PHONE_1,
                parent_uuid=self.top_tenant_uuid,
                address=has_entries(**ADDRESS_1),
                domain_names=contains_inanyorder(*VALID_DOMAIN_NAMES_1),
                default_authentication_method='native',
            ),
        )

        accent_all_users_groups = self.client.groups.list(
            search='accent-all-users', recurse=True
        )['items']
        assert_that(
            accent_all_users_groups,
            contains_inanyorder(
                has_entries(
                    name=f'accent-all-users-tenant-{self.top_tenant_uuid}',
                    tenant_uuid=self.top_tenant_uuid,
                ),
                has_entries(
                    name=f'accent-all-users-tenant-{foobar["uuid"]}',
                    tenant_uuid=foobar['uuid'],
                ),
                has_entries(
                    name=f'accent-all-users-tenant-{foobaz["uuid"]}',
                    tenant_uuid=foobaz['uuid'],
                ),
                has_entries(
                    name=f'accent-all-users-tenant-{other["uuid"]}',
                    tenant_uuid=other['uuid'],
                ),
            ),
        )

        def expected_policies(tenant_uuid):
            return contains_exactly(
                has_entries(
                    slug=ALL_USERS_POLICY_SLUG,
                    tenant_uuid=tenant_uuid,
                    acl=has_item('integration_tests.access'),
                )
            )

        # Assert default policies from admin point of view (recurse=True)
        accent_all_users_policies = [
            {
                'group': accent_all_users_group,
                'policies': self.client.groups.get_policies(
                    accent_all_users_group['uuid'], recurse=True
                )['items'],
            }
            for accent_all_users_group in accent_all_users_groups
        ]

        assert_that(
            accent_all_users_policies,
            contains_inanyorder(
                has_entries(
                    group=has_entries(tenant_uuid=self.top_tenant_uuid),
                    policies=expected_policies(self.top_tenant_uuid),
                ),
                has_entries(
                    group=has_entries(tenant_uuid=foobar['uuid']),
                    policies=expected_policies(self.top_tenant_uuid),
                ),
                has_entries(
                    group=has_entries(tenant_uuid=foobaz['uuid']),
                    policies=expected_policies(self.top_tenant_uuid),
                ),
                has_entries(
                    group=has_entries(tenant_uuid=other['uuid']),
                    policies=expected_policies(self.top_tenant_uuid),
                ),
            ),
        )

        # Assert default policies from tenant point of view
        result = []
        for group in accent_all_users_groups:
            self.client.tenant_uuid = group['tenant_uuid']
            policies = self.client.groups.get_policies(group['uuid'])['items']
            self.client.tenant_uuid = None
            result.append({'group': group, 'policies': policies})

        assert_that(
            result,
            contains_inanyorder(
                has_entries(
                    group=has_entries(tenant_uuid=self.top_tenant_uuid),
                    policies=expected_policies(self.top_tenant_uuid),
                ),
                has_entries(
                    group=has_entries(tenant_uuid=foobar['uuid']),
                    policies=expected_policies(foobar['uuid']),
                ),
                has_entries(
                    group=has_entries(tenant_uuid=foobaz['uuid']),
                    policies=expected_policies(foobaz['uuid']),
                ),
                has_entries(
                    group=has_entries(tenant_uuid=other['uuid']),
                    policies=expected_policies(other['uuid']),
                ),
            ),
        )

        tenant_uuids = [
            self.top_tenant_uuid,
            foobar['uuid'],
            foobaz['uuid'],
            other['uuid'],
        ]
        slug = ALL_USERS_POLICY_SLUG
        for tenant_uuid in tenant_uuids:
            assert_that(
                self.client.policies.list(tenant_uuid=tenant_uuid)['items'],
                has_item(has_entries(slug=slug, tenant_uuid=tenant_uuid)),
            )

        params = {'name': 'subtenant', 'parent_uuid': foobar['uuid']}
        with self.tenant(self.client, **params) as subtenant:
            assert_that(subtenant, has_entries(uuid=uuid_(), **params))

    def test_tenant_created_event(self):
        headers = {'name': 'auth_tenant_added'}
        msg_accumulator = self.bus.accumulator(headers=headers)
        name = 'My tenant'
        slug = 'my_tenant'
        tenant = self.client.tenants.new(
            name=name, slug=slug, domain_names=VALID_DOMAIN_NAMES_1
        )

        def bus_received_msg():
            assert_that(
                msg_accumulator.accumulate(with_headers=True),
                contains_exactly(
                    has_entries(
                        message=has_entries(
                            name='auth_tenant_added',
                            data=has_entries(
                                name=name,
                                slug=slug,
                                domain_names=contains_inanyorder(*VALID_DOMAIN_NAMES_1),
                            ),
                        ),
                        headers=has_entry('tenant_uuid', tenant['uuid']),
                    )
                ),
            )

        try:
            until.assert_(bus_received_msg, tries=10, interval=0.25)
        finally:
            self.client.tenants.delete(tenant['uuid'])

    @fixtures.http.tenant(slug='dup')
    def test_post_duplicate_slug(self, a):
        assert_http_error(409, self.client.tenants.new, slug='dup')

    @fixtures.http.tenant(domain_names=VALID_DOMAIN_NAMES_1)
    def test_post_duplicate_domain_names(self, a):
        assert_http_error(409, self.client.tenants.new, domain_names=['accentvoice.io'])

    def test_post_invalid_domain_names(self):
        invalid_domain_names = [
            ['-accentvoice.io'],
            [' accentvoice.io'],
            ['#'],
            ['123'],
            ['accent .io'],
            ['accentvoice.io-'],
            ['accent'],
            ['=accentvoice.io'],
            ['+accentvoice.io'],
            ['_accentvoice.io'],
            ['accent_io'],
            ['accent_io  '],
            None,
            True,
            False,
            'accentvoice.io',
            42,
            {'name': 'accentvoice.io'},
        ]
        for invalid_domain_name in invalid_domain_names:
            assert_http_error(
                400, self.client.tenants.new, domain_names=invalid_domain_name
            )

    def test_post_invalid_default_authentication_method(self):
        invalid_values = [
            None,
            False,
            True,
            42,
            ['native'],
            'not-native',
            '',
        ]
        for invalid_auth_method in invalid_values:
            assert_http_error(
                400,
                self.client.tenants.new,
                default_authentication_method=invalid_auth_method,
            )

    @fixtures.http.tenant(domain_names=VALID_DOMAIN_NAMES_2)
    def test_delete(self, tenant):
        with self.client_in_subtenant() as (client, user, sub_tenant):
            assert_http_error(404, client.tenants.delete, tenant['uuid'])
            assert_http_error(403, client.tenants.delete, sub_tenant['uuid'])

        assert_no_error(self.client.tenants.delete, tenant['uuid'])
        assert_http_error(404, self.client.tenants.delete, tenant['uuid'])

    @fixtures.http.tenant(domain_names=VALID_DOMAIN_NAMES_2)
    def test_tenant_deleted_event(self, tenant):
        headers = {'name': 'auth_tenant_deleted'}
        msg_accumulator = self.bus.accumulator(headers=headers)

        self.client.tenants.delete(tenant['uuid'])

        def bus_received_msg():
            assert_that(
                msg_accumulator.accumulate(with_headers=True),
                contains_exactly(
                    has_entries(
                        message=has_entries(
                            name='auth_tenant_deleted',
                            data=has_entries(
                                uuid=tenant['uuid'],
                            ),
                        ),
                        headers=has_entry('tenant_uuid', tenant['uuid']),
                    )
                ),
            )

        until.assert_(bus_received_msg, tries=10, interval=0.25)

    @fixtures.http.tenant(domain_names=VALID_DOMAIN_NAMES_3)
    def test_delete_tenant_with_children(self, tenant):
        with self.client_in_subtenant(parent_uuid=tenant['uuid']) as (
            client,
            user,
            sub_tenant,
        ):
            assert_http_error(400, self.client.tenants.delete, tenant['uuid'])

    @fixtures.http.tenant(address=ADDRESS_1)
    def test_get_one(self, tenant):
        with self.client_in_subtenant() as (client, user, sub_tenant):
            assert_http_error(404, client.tenants.get, tenant['uuid'])
            result = client.tenants.get(sub_tenant['uuid'])
            assert_that(result, equal_to(sub_tenant))

        result = self.client.tenants.get(tenant['uuid'])
        assert_that(result, equal_to(tenant))

        assert_http_error(404, self.client.tenants.get, UNKNOWN_UUID)

    @fixtures.http.tenant(name='foobar', slug='aaa', domain_names=VALID_DOMAIN_NAMES_1)
    @fixtures.http.tenant(name='foobaz', slug='bbb', domain_names=VALID_DOMAIN_NAMES_2)
    @fixtures.http.tenant(
        name='foobarbaz', slug='ccc', domain_names=VALID_DOMAIN_NAMES_3
    )
    # extra tenant: "master" tenant
    def test_list(self, foobar, foobaz, foobarbaz):
        top_tenant = self.get_top_tenant()

        def then(
            result, total=4, filtered=4, item_matcher=contains_exactly(top_tenant)
        ):
            assert_that(
                result, has_entries(items=item_matcher, total=total, filtered=filtered)
            )

        foobaz_uuid = foobaz['uuid']
        foobar_uuid = foobar['uuid']
        foobar['domain_names'] = contains_inanyorder(*foobar['domain_names'])
        foobaz['domain_names'] = contains_inanyorder(*foobaz['domain_names'])
        foobarbaz['domain_names'] = contains_inanyorder(*foobarbaz['domain_names'])
        foobar = has_entries(**foobar)
        foobaz = has_entries(**foobaz)
        foobarbaz = has_entries(**foobarbaz)

        result = self.client.tenants.list()
        matcher = contains_inanyorder(foobaz, foobar, foobarbaz, top_tenant)
        then(result, item_matcher=matcher)

        result = self.client.tenants.list(uuid=foobaz_uuid)
        matcher = contains_inanyorder(foobaz)
        then(result, filtered=1, item_matcher=matcher)

        result = self.client.tenants.list(uuids=[foobaz_uuid, foobar_uuid])
        matcher = contains_inanyorder(foobaz, foobar)
        then(result, filtered=2, item_matcher=matcher)

        assert_http_error(
            400, self.client.tenants.list, uuids=[str(uuid4()) for _ in range(26)]
        )

        result = self.client.tenants.list(slug='ccc')
        matcher = contains_inanyorder(foobarbaz)
        then(result, filtered=1, item_matcher=matcher)

        result = self.client.tenants.list(domain_name='outlook.fr')
        matcher = contains_inanyorder(foobarbaz)
        then(result, filtered=1, item_matcher=matcher)

        result = self.client.tenants.list(search='yahoo')
        matcher = contains_inanyorder(foobaz, foobarbaz)
        then(result, filtered=2, item_matcher=matcher)

        result = self.client.tenants.list(search='bar')
        matcher = contains_inanyorder(foobar, foobarbaz)
        then(result, filtered=2, item_matcher=matcher)

        result = self.client.tenants.list(search='bbb')
        matcher = contains_inanyorder(foobaz)
        then(result, filtered=1, item_matcher=matcher)

        result = self.client.tenants.list(limit=1, offset=1, order='name')
        matcher = contains_exactly(foobarbaz)
        then(result, item_matcher=matcher)

        result = self.client.tenants.list(order='slug')
        matcher = contains_exactly(
            foobar, foobaz, foobarbaz, has_entries(slug='master')
        )
        then(result, item_matcher=matcher)

        result = self.client.tenants.list(order='name', direction='desc')
        matcher = contains_exactly(top_tenant, foobaz, foobarbaz, foobar)
        then(result, item_matcher=matcher)

        assert_http_error(400, self.client.tenants.list, limit='foo')
        assert_http_error(400, self.client.tenants.list, offset=-1)

        with self.client_in_subtenant() as (client, user, sub_tenant):
            with self.tenant(client, name='subsub') as subsub:
                result = client.tenants.list()
                matcher = contains_exactly(sub_tenant, subsub)
                then(result, total=2, filtered=2, item_matcher=matcher)

    @fixtures.http.tenant()
    @fixtures.http.user()
    def test_put(self, tenant, user):
        name = 'foobar'
        body = {
            'name': name,
            'address': ADDRESS_1,
            'contact': user['uuid'],
            'default_authentication_method': 'ldap',
        }
        body_with_unknown_contact = dict(body)
        body_with_unknown_contact['contact'] = UNKNOWN_UUID
        invalid_auth_methods = [
            None,
            False,
            True,
            42,
            ['native'],
            'not-native',
            '',
        ]

        with self.client_in_subtenant() as (client, _, sub_tenant):
            assert_http_error(404, client.tenants.edit, tenant['uuid'], **body)
            assert_no_error(client.tenants.edit, sub_tenant['uuid'], **body)

        for auth_method in invalid_auth_methods:
            assert_http_error(
                400,
                self.client.tenants.edit,
                tenant['uuid'],
                default_authentication_method=auth_method,
            )
        assert_http_error(400, self.client.tenants.edit, tenant['uuid'], name=False)
        assert_http_error(404, self.client.tenants.edit, UNKNOWN_UUID, **body)
        assert_http_error(
            404, self.client.tenants.edit, tenant['uuid'], **body_with_unknown_contact
        )

        result = self.client.tenants.edit(tenant['uuid'], **body)

        assert_that(
            result,
            has_entries(
                uuid=tenant['uuid'],
                name=name,
                contact=user['uuid'],
                address=has_entries(**ADDRESS_1),
                default_authentication_method='ldap',
            ),
        )

    @fixtures.http.tenant(name='foobar')
    def test_put_event(self, tenant):
        headers = {'name': 'auth_tenant_updated'}
        msg_accumulator = self.bus.accumulator(headers=headers)

        assert_no_error(self.client.tenants.edit, tenant['uuid'], name='foo')

        def bus_received_msg():
            assert_that(
                msg_accumulator.accumulate(with_headers=True),
                has_item(
                    has_entries(
                        message=has_entries(
                            data=has_entries(
                                uuid=tenant['uuid'],
                                name='foo',
                            ),
                        ),
                        headers=has_entries(
                            name='auth_tenant_updated',
                            tenant_uuid=tenant['uuid'],
                        ),
                    )
                ),
            )

        until.assert_(bus_received_msg, tries=10, interval=0.25)

    @fixtures.http.tenant(domain_names=VALID_DOMAIN_NAMES_1)
    @fixtures.http.user()
    def test_put_updated_domain_names(self, tenant, user):
        name = 'foobar'
        body = {
            'name': name,
            'address': ADDRESS_1,
            'contact': user['uuid'],
            'domain_names': ['accentvoice.io'],
        }

        result = self.client.tenants.edit(tenant['uuid'], **body)

        assert_that(
            result,
            has_entries(
                uuid=tenant['uuid'],
                name=name,
                contact=user['uuid'],
                address=has_entries(**ADDRESS_1),
                domain_names=['accentvoice.io'],
            ),
        )

    @fixtures.http.tenant(domain_names=VALID_DOMAIN_NAMES_1)
    @fixtures.http.tenant(domain_names=VALID_DOMAIN_NAMES_2)
    def test_put_duplicate_domain_names_raises_409(self, tenant_1, tenant_2):
        name = 'foobar'
        body = {
            'name': name,
            'domain_names': ['accentvoice.io'],
        }

        assert_http_error(409, self.client.tenants.edit, tenant_2['uuid'], **body)

    @fixtures.http.tenant(slug='ABC')
    def test_put_slug_is_read_only(self, tenant):
        new_body = dict(tenant)
        new_body['slug'] = 'DEF'

        result = self.client.tenants.edit(tenant['uuid'], **new_body)

        assert_that(result, has_entries(**tenant))

    @fixtures.http.tenant(domain_names=VALID_DOMAIN_NAMES_1)
    @fixtures.http.tenant(domain_names=[])
    def test_get_domains(self, tenant_1, tenant_2):

        result = self.client.tenants.get_domains(tenant_1['uuid'])
        assert_that(result['total'], is_(2))
        assert_that(
            result['items'],
            contains_inanyorder(
                has_entries({'name': VALID_DOMAIN_NAMES_1[0], 'uuid': uuid_()}),
                has_entries({'name': VALID_DOMAIN_NAMES_1[1], 'uuid': uuid_()}),
            ),
        )

        result = self.client.tenants.get_domains(tenant_2['uuid'])
        assert_that(result['total'], is_(0))
        assert_that(result['items'], empty())

        assert_http_error(404, self.client.tenants.get_domains, UNKNOWN_UUID)
