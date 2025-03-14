# Copyright 2023 Accent Communications

import time
from collections import namedtuple

import ldap
from accent_test_helpers.hamcrest.uuid_ import uuid_
from hamcrest import assert_that, has_entries
from ldap.modlist import addModlist

from .helpers import base, fixtures
from .helpers.base import assert_http_error

Contact = namedtuple(
    'Contact',
    [
        'cn',
        'uid',
        'password',
        'mail',
        'login_attribute',
        'employee_type',
        'search_only',
    ],
)

TENANT_1_UUID = '2ec55cd6-c465-47a9-922f-569b404c48b8'
TENANT_2_UUID = '402f2ee0-2af9-4b87-80ce-9d9e94f620e5'
LDAP_PORT = 1389

LDAP_KWARGS = {
    'host': 'slapd',
    'port': LDAP_PORT,
    'bind_dn': 'cn=accent_auth,ou=people,dc=accent-auth,dc=accent,dc=community',
    'bind_password': 'S3cr$t',  # NOSONAR
    'user_base_dn': 'ou=quebec,ou=people,dc=accent-auth,dc=accent,dc=community',
    'user_login_attribute': 'mail',
    'user_email_attribute': 'mail',
}


class LDAPHelper:
    BASE_DN = 'dc=accent-auth,dc=accent,dc=community'
    ADMIN_DN = f'cn=admin,{BASE_DN}'
    ADMIN_PASSWORD = 'accentpassword'
    PEOPLE_DN = f'ou=people,{BASE_DN}'
    QUEBEC_DN = f'ou=quebec,{PEOPLE_DN}'
    OU_DN = {'people': PEOPLE_DN, 'quebec': QUEBEC_DN}
    CONFIG_DN = 'cn=config'
    CONFIG_DATABASE_DN = f'olcDatabase={{2}}mdb,{CONFIG_DN}'
    CONFIG_ADMIN_DN = f'cn=admin,{CONFIG_DN}'
    CONFIG_ADMIN_PASSWORD = 'configpassword'
    setup_ran = False

    def __init__(self, ldap_uri):
        self._ldap_obj = ldap.initialize(ldap_uri)
        self._ldap_obj.simple_bind_s(self.ADMIN_DN, self.ADMIN_PASSWORD)
        self._ldap_admin_obj = ldap.initialize(ldap_uri)
        self._ldap_admin_obj.simple_bind_s(
            self.CONFIG_ADMIN_DN, self.CONFIG_ADMIN_PASSWORD
        )

    def add_contact(self, contact, ou):
        dn = f'cn={contact.cn},{self.OU_DN[ou]}'
        modlist = addModlist(
            {
                'objectClass': [b'inetOrgPerson'],
                'cn': [contact.cn.encode('utf-8')],
                'sn': [contact.cn.encode('utf-8')],
                'uid': [contact.uid.encode('utf-8')],
                'userPassword': [contact.password.encode('utf-8')],
                'mail': [contact.mail.encode('utf-8')],
                'employeeType': [contact.employee_type.encode('utf-8')],
            }
        )

        self._ldap_obj.add_s(dn, modlist)

    def add_contact_without_email(self, contact, ou):
        dn = f'cn={contact.cn},{self.OU_DN[ou]}'
        modlist = addModlist(
            {
                'objectClass': [b'inetOrgPerson'],
                'cn': [contact.cn.encode('utf-8')],
                'sn': [contact.cn.encode('utf-8')],
                'uid': [contact.uid.encode('utf-8')],
                'userPassword': [contact.password.encode('utf-8')],
                'employeeType': [contact.employee_type.encode('utf-8')],
            }
        )

        self._ldap_obj.add_s(dn, modlist)

    def add_ou(self):
        modlist = addModlist(
            {'objectClass': [b'organizationalUnit'], 'ou': [b'people']}
        )
        self._ldap_obj.add_s(self.PEOPLE_DN, modlist)
        modlist = addModlist(
            {'objectClass': [b'organizationalUnit'], 'ou': [b'quebec']}
        )
        self._ldap_obj.add_s(self.QUEBEC_DN, modlist)

    def add_acl(self, contact, affected_ou, acl):
        _, old_config = self._ldap_admin_obj.search_ext_s(
            self.CONFIG_DATABASE_DN, ldap.SCOPE_SUBTREE
        )[0]

        new_config = old_config.copy()
        ou = self.OU_DN[affected_ou]
        user_dn = f'cn={contact.cn},{ou}'

        new_config['olcAccess'] = new_config.get('olcAccess', [])
        acls = new_config['olcAccess']
        acls.insert(
            0, f'to attrs=mail by dn.exact="{user_dn}" {acl} by * write'.encode()
        )
        acls.append(b'to * by self read by users read by * read')
        self._ldap_admin_obj.add_s(self.CONFIG_DATABASE_DN, addModlist(new_config))


@base.use_asset('base')
class BaseLDAPIntegrationTest(base.BaseIntegrationTest):
    asset_cls = base.APIAssetLaunchingTestCase
    username = 'admin'
    password = 's3cre7'

    CONTACTS = [
        Contact(
            cn='Alice Wonderland',
            uid='awonderland',
            password='awonderland_password',
            mail='awonderland@accent-auth.com',
            login_attribute='cn',
            employee_type='human',
            search_only=False,
        ),
        Contact(
            cn='Jack Sparrow',
            uid='jsparrow',
            password='jsparrow_password',
            mail='jsparrow@accent-auth.com',
            login_attribute='cn',
            employee_type='human',
            search_only=False,
        ),
        Contact(
            cn='Boba Fett',
            uid='bfett',
            password='bobafett_password',
            mail='bobaFett@accent-auth.com',
            login_attribute='mail',
            employee_type='human',
            search_only=False,
        ),
        Contact(
            cn='Humpty Dumpty',
            uid='humptydumpty',
            password='humptydumpty_password',
            mail=None,
            login_attribute='uid',
            employee_type='human',
            search_only=False,
        ),
        Contact(
            cn='Lewis Carroll',
            uid='lewiscarroll',
            password='lewiscarroll_password',
            mail='lewiscarroll@accent-auth.com',
            login_attribute='mail',
            employee_type='human',
            search_only=False,
        ),
        Contact(
            cn='The Cheshire Cat',
            uid='cheshirecat',
            password='cheshirecat_password',
            mail='cheshirecat@accent-auth.com',
            login_attribute='mail',
            employee_type='animal',
            search_only=False,
        ),
        Contact(
            cn='The White Queen',
            uid='whitequeen',
            password='whitequeen_password',
            mail='whitequeen@accent-auth.com',
            login_attribute='mail',
            employee_type='human',
            search_only=True,
        ),
    ]

    @classmethod
    def add_contacts(cls, contacts, ldap_helper):
        ldap_helper.add_ou()
        ldap_helper.add_contact(
            Contact('accent_auth', 'accent_auth', 'S3cr$t', '', 'cn', 'service', False),
            'people',
        )
        for contact in contacts:
            if not contact.mail:
                ldap_helper.add_contact_without_email(contact, 'quebec')
            else:
                ldap_helper.add_contact(contact, 'quebec')

            if contact.search_only:
                ldap_helper.add_acl(contact, 'quebec', 'search')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        ldap_host = '127.0.0.1'
        ldap_port = cls.asset_cls.service_port(LDAP_PORT, 'slapd')
        ldap_uri = f'ldap://{ldap_host}:{ldap_port}'

        for _ in range(10):
            try:
                helper = LDAPHelper(ldap_uri)
                break
            except ldap.SERVER_DOWN:
                time.sleep(1)
        else:
            raise Exception('could not add contacts: LDAP server is down')
        if not LDAPHelper.setup_ran:
            cls.add_contacts(cls.CONTACTS, helper)
            LDAPHelper.setup_ran = True


@base.use_asset('base')
class TestLDAP(BaseLDAPIntegrationTest):
    def setUp(self):
        ldap_config = self.client.ldap_config.update(
            {
                'host': 'slapd',
                'port': LDAP_PORT,
                'user_base_dn': 'ou=quebec,ou=people,dc=accent-auth,dc=accent,dc=community',
                'user_login_attribute': 'cn',
                'user_email_attribute': 'mail',
            },
            tenant_uuid=self.top_tenant_uuid,
        )
        self.addCleanup(self.client.ldap_config.delete, ldap_config['tenant_uuid'])

    @fixtures.http.tenant(
        uuid=TENANT_1_UUID,
        slug='mytenant',
        domain_names=['accentvoice.io'],
        default_authentication_method='ldap',
    )
    @fixtures.http.user(
        email_address='jsparrow@accent-auth.com',
        tenant_uuid=TENANT_1_UUID,
        authentication_method='ldap',
    )
    @fixtures.http.user(
        email_address='BObAFett@accent-auth.com',
        tenant_uuid=TENANT_1_UUID,
        authentication_method='ldap',
    )
    @fixtures.http.ldap_config(tenant_uuid=TENANT_1_UUID, **LDAP_KWARGS)
    def test_ldap_authentication_works_when_login_with_case_sensitive_email_address(
        self, tenant, user1, user2, _
    ):
        response = self._post_token(
            'JSparrow@ACCENT-auth.com',
            'jsparrow_password',
            domain_name=tenant['domain_names'][0],
        )
        assert_that(
            response, has_entries(metadata=has_entries(pbx_user_uuid=user1['uuid']))
        )

        response = self._post_token(
            'bobafett@accent-auth.com',
            'bobafett_password',
            domain_name=tenant['domain_names'][0],
        )

    @fixtures.http.tenant(
        uuid=TENANT_1_UUID,
        slug='mytenant',
        domain_names=['accentvoice.io', 'cust-42.myclients.com'],
        default_authentication_method='ldap',
    )
    @fixtures.http.user(username='bobafett@accent-auth.com', tenant_uuid=TENANT_1_UUID)
    @fixtures.http.ldap_config(tenant_uuid=TENANT_1_UUID, **LDAP_KWARGS)
    def test_ldap_authentication_when_user_has_no_email_address_but_username(
        self, tenant, user, _
    ):
        response = self._post_token(
            'bobafett@accent-auth.com',
            'bobafett_password',
            domain_name=tenant['domain_names'][0],
        )
        assert_that(
            response, has_entries(metadata=has_entries(pbx_user_uuid=user['uuid']))
        )

    @fixtures.http.tenant(
        uuid=TENANT_1_UUID,
        slug='mytenant',
        domain_names=['accentvoice.io', 'cust-42.myclients.com'],
        default_authentication_method='native',
    )
    @fixtures.http.user(
        username='bobafett@accent-auth.com',
        tenant_uuid=TENANT_1_UUID,
        authentication_method='default',
    )
    @fixtures.http.user(
        email_address='jsparrow@accent-auth.com',
        tenant_uuid=TENANT_1_UUID,
        authentication_method='ldap',
    )
    @fixtures.http.ldap_config(tenant_uuid=TENANT_1_UUID, **LDAP_KWARGS)
    def test_ldap_authentication_when_not_authorized(
        self,
        tenant,
        *_,
    ):
        # tenant = native, user = default
        assert_http_error(
            401,
            self._post_token,
            'bobafett@accent-auth.com',
            'bobafett_password',
            domain_name=tenant['domain_names'][0],
        )

        # tenant = native, user = ldap
        response = self._post_token(
            'JSparrow@ACCENT-auth.com',
            'jsparrow_password',
            tenant_id=tenant['slug'],
        )
        assert_that(response, has_entries(token=uuid_()))

        tenant['default_authentication_method'] = 'ldap'
        self.client.tenants.edit(tenant['uuid'], **tenant)

        # tenant = ldap, user = default
        response = self._post_token(
            'bobafett@accent-auth.com',
            'bobafett_password',
            tenant_id=tenant['slug'],
        )
        assert_that(response, has_entries(token=uuid_()))

    @fixtures.http.tenant(
        uuid=TENANT_1_UUID,
        slug='mytenant',
        domain_names=['accentvoice.io', 'cust-42.myclients.com'],
        default_authentication_method='ldap',
    )
    @fixtures.http.user(
        email_address='awonderland@accent-auth.com', tenant_uuid=TENANT_1_UUID
    )
    @fixtures.http.ldap_config(
        tenant_uuid=TENANT_1_UUID,
        host='slapd',
        port=LDAP_PORT,
        user_base_dn='ou=quebec,ou=people,dc=accent-auth,dc=accent,dc=community',
        user_login_attribute='cn',
        user_email_attribute='mail',
    )
    def test_ldap_authentication_with_tenant_id_and_domain_name(self, tenant, user, _):
        response = self._post_token(
            'Alice Wonderland',
            'awonderland_password',
            tenant_id=tenant['uuid'],
        )
        assert_that(
            response, has_entries(metadata=has_entries(pbx_user_uuid=user['uuid']))
        )

        response = self._post_token(
            'Alice Wonderland',
            'awonderland_password',
            tenant_id=tenant['slug'],
        )
        assert_that(
            response, has_entries(metadata=has_entries(pbx_user_uuid=user['uuid']))
        )

        response = self._post_token(
            'Alice Wonderland',
            'awonderland_password',
            domain_name='cust-42.myclients.com',
        )
        assert_that(
            response, has_entries(metadata=has_entries(pbx_user_uuid=user['uuid']))
        )

        assert_http_error(
            400,
            self._post_token,
            'Alice Wonderland',
            'awonderland_password',
            tenant_id=tenant['uuid'],
            domain_name='cust-42.myclients.com',
        )

    @fixtures.http.user(
        email_address='whitequeen@accent-auth.com',
        authentication_method='ldap',
    )
    def test_ldap_authentication_user_cannot_read_ldap_email(self, _):
        assert_http_error(
            401,
            self._post_token,
            'The White Queen',
            'whitequeen_password',
            tenant_id=self.top_tenant_uuid,
        )

    @fixtures.http.tenant(
        uuid=TENANT_1_UUID,
        default_authentication_method='ldap',
    )
    @fixtures.http.user(
        email_address='lewiscarroll@accent-auth.com',
        tenant_uuid=TENANT_1_UUID,
    )
    @fixtures.http.tenant(
        uuid=TENANT_2_UUID,
        default_authentication_method='ldap',
    )
    @fixtures.http.ldap_config(
        tenant_uuid=TENANT_2_UUID,
        host='slapd',
        port=LDAP_PORT,
        bind_dn='cn=accent_auth,ou=people,dc=accent-auth,dc=accent,dc=community',
        bind_password='S3cr$t',
        user_base_dn='dc=accent-auth,dc=accent,dc=community',
        user_login_attribute='mail',
        user_email_attribute='mail',
    )
    def test_ldap_authentication_multi_tenant(self, _, __, tenant2, ___):
        assert_http_error(
            401,
            self._post_token,
            'Lewis Carroll',
            'lewiscarroll_password',
            tenant_id=tenant2['slug'],
        )

    @fixtures.http.user(
        email_address='awonderland@accent-auth.com',
        authentication_method='ldap',
    )
    def test_ldap_authentication_fail_when_wrong_password(self, _):
        assert_http_error(
            401,
            self._post_token,
            'Alice Wonderland',
            'wrong_password',
            tenant_id=self.top_tenant_uuid,
        )

    @fixtures.http.user(
        email_address='humptydumpty@accent-auth.com',
        authentication_method='ldap',
    )
    def test_ldap_authentication_fails_when_no_email_in_ldap(self, _):
        assert_http_error(
            401,
            self._post_token,
            'Humpty Dumpty',
            'humptydumpty_password',
            tenant_id=self.top_tenant_uuid,
        )

    @fixtures.http.user(
        email_address=None,
        authentication_method='ldap',
    )
    def test_ldap_authentication_fails_when_no_email_in_user(self, _):
        assert_http_error(
            401,
            self._post_token,
            'Lewis Carroll',
            'lewiscarroll_password',
            tenant_id=self.top_tenant_uuid,
        )


@base.use_asset('base')
class TestLDAPServiceUser(BaseLDAPIntegrationTest):
    def setUp(self):
        ldap_config = self.client.ldap_config.update(
            {
                'host': 'slapd',
                'port': LDAP_PORT,
                'bind_dn': 'cn=accent_auth,ou=people,dc=accent-auth,dc=accent,dc=community',
                'bind_password': 'S3cr$t',
                'user_base_dn': 'dc=accent-auth,dc=accent,dc=community',
                'user_login_attribute': 'uid',
                'user_email_attribute': 'mail',
                'search_filters': '(&({user_login_attribute}={username})(employeeType=human))',
            },
            tenant_uuid=self.top_tenant_uuid,
        )
        self.addCleanup(self.client.ldap_config.delete, ldap_config['tenant_uuid'])

    @fixtures.http.user(
        email_address='awonderland@accent-auth.com',
        authentication_method='ldap',
    )
    def test_ldap_authentication(self, user):
        response = self._post_token(
            'awonderland',
            'awonderland_password',
            tenant_id=self.top_tenant_uuid,
        )
        assert_that(
            response, has_entries(metadata=has_entries(pbx_user_uuid=user['uuid']))
        )

    @fixtures.http.user(
        email_address='whitequeen@accent-auth.com',
        authentication_method='ldap',
    )
    def test_ldap_authentication_user_cannot_read_ldap_email(self, user):
        response = self._post_token(
            'whitequeen',
            'whitequeen_password',
            tenant_id=self.top_tenant_uuid,
        )
        assert_that(
            response, has_entries(metadata=has_entries(pbx_user_uuid=user['uuid']))
        )

    @fixtures.http.tenant(
        uuid=TENANT_1_UUID,
        default_authentication_method='ldap',
    )
    @fixtures.http.user(
        email_address='lewiscarroll@accent-auth.com',
        tenant_uuid=TENANT_1_UUID,
    )
    @fixtures.http.tenant(
        uuid=TENANT_2_UUID,
        default_authentication_method='ldap',
    )
    @fixtures.http.ldap_config(
        tenant_uuid=TENANT_2_UUID,
        host='slapd',
        port=LDAP_PORT,
        bind_dn='cn=accent_auth,ou=people,dc=accent-auth,dc=accent,dc=community',
        bind_password='S3cr$t',
        user_base_dn='dc=accent-auth,dc=accent,dc=community',
        user_login_attribute='mail',
        user_email_attribute='mail',
    )
    def test_ldap_authentication_multi_tenant(self, _, __, tenant2, ___):
        assert_http_error(
            401,
            self._post_token,
            'lewiscarroll@accent-auth.com',
            'lewiscarroll_password',
            tenant_id=tenant2['slug'],
        )

    @fixtures.http.user(
        email_address='awonderland@accent-auth.com',
        authentication_method='ldap',
    )
    def test_ldap_authentication_fail_when_wrong_password(self, _):
        assert_http_error(
            401,
            self._post_token,
            'awonderland',
            'wrong_password',
            tenant_id=self.top_tenant_uuid,
        )

    @fixtures.http.user(
        email_address='humptydumpty@accent-auth.com',
        authentication_method='ldap',
    )
    def test_ldap_authentication_fails_when_no_email_in_ldap(self, _):
        assert_http_error(
            401,
            self._post_token,
            'humptydumpty',
            'humptydumpty_password',
            tenant_id=self.top_tenant_uuid,
        )

    @fixtures.http.user(
        email_address=None,
        authentication_method='ldap',
    )
    def test_ldap_authentication_fails_when_no_email_in_user(self, _):
        assert_http_error(
            401,
            self._post_token,
            'lewiscarroll',
            'lewiscarroll_password',
            tenant_id=self.top_tenant_uuid,
        )

    @fixtures.http.user(
        email_address='cheshirecat@accent-auth.com',
        authentication_method='ldap',
    )
    def test_ldap_authentication_search_filter_does_not_match_employee_type(self, _):
        assert_http_error(
            401,
            self._post_token,
            'cheshirecat',
            'cheshirecat_password',
            tenant_id=self.top_tenant_uuid,
        )


@base.use_asset('base')
class TestLDAPRefreshToken(BaseLDAPIntegrationTest):
    def setUp(self):
        ldap_config = self.client.ldap_config.update(
            {
                'host': 'slapd',
                'port': LDAP_PORT,
                'user_base_dn': 'ou=quebec,ou=people,dc=accent-auth,dc=accent,dc=community',
                'user_login_attribute': 'cn',
                'user_email_attribute': 'mail',
            },
            tenant_uuid=self.top_tenant_uuid,
        )
        self.addCleanup(self.client.ldap_config.delete, ldap_config['tenant_uuid'])

    @fixtures.http.user(
        email_address='awonderland@accent-auth.com',
        authentication_method='ldap',
    )
    def test_ldap_login_with_refresh_token(self, user):
        client_id = 'my-test'
        args = ('Alice Wonderland', 'awonderland_password')
        refresh_token = self._post_token(
            *args,
            client_id=client_id,
            access_type='offline',
            tenant_id=self.top_tenant_uuid,
        )['refresh_token']

        response = self._post_token(
            None,
            None,
            expiration=1,
            refresh_token=refresh_token,
            client_id=client_id,
            tenant_id=self.top_tenant_uuid,
        )
        assert_that(
            response, has_entries(metadata=has_entries(pbx_user_uuid=user['uuid']))
        )
