# Copyright 2023 Accent Communications

from contextlib import contextmanager

from accent_test_helpers.hamcrest.raises import raises
from hamcrest import (
    assert_that,
    calling,
    contains_exactly,
    contains_inanyorder,
    empty,
    equal_to,
    has_properties,
    not_,
)

from accent_auth import exceptions

from .helpers import base, fixtures
from .helpers.constants import UNKNOWN_SLUG, UNKNOWN_UUID

TENANT_UUID_1 = '00000000-0000-4000-a000-000000000001'
TENANT_UUID_2 = '00000000-0000-4000-a000-000000000002'
TENANT_UUID_3 = '00000000-0000-4000-a000-000000000003'
TENANT_UUID_4 = '00000000-0000-4000-a000-000000000004'


@base.use_asset('database')
class TestPolicyDAO(base.DAOTestCase):
    def setUp(self):
        super().setUp()
        master_policy = self._policy_dao.find_by(name='accent_default_master_user_policy')
        self._default_master_user_policy_uuid = master_policy.uuid

    @fixtures.db.policy(name='testé', description='déscription')
    def test_access_association(self, uuid):
        self._policy_dao.associate_access(uuid, '#')
        policy = self._policy_dao.find_by(uuid=uuid)
        assert_that(policy, has_properties(acl=contains_inanyorder('#')))

        assert_that(
            calling(self._policy_dao.associate_access).with_args(uuid, '#'),
            raises(exceptions.DuplicateAccessException),
        )

        self._policy_dao.dissociate_access(uuid, '#')
        policy = self._policy_dao.find_by(uuid=uuid)
        assert_that(policy, has_properties(acl=empty()))

        assert_that(
            calling(self._policy_dao.associate_access).with_args('unknown', '#'),
            raises(exceptions.UnknownPolicyException),
        )
        self._policy_dao.dissociate_access('unknown', '#')

    @fixtures.db.tenant()
    def test_create(self, tenant_uuid):
        acl = ['dird.#', 'confd.line.42.*']
        body = {
            'name': 'testé',
            'slug': 'teste',
            'description': 'descriptioñ',
            'acl': acl,
            'tenant_uuid': tenant_uuid,
        }
        with self._new_policy(**body) as uuid_:
            policy = self._policy_dao.find_by(uuid=uuid_)

            assert_that(
                policy,
                has_properties(
                    uuid=uuid_,
                    name='testé',
                    description='descriptioñ',
                    acl=contains_inanyorder(*acl),
                    tenant_uuid=tenant_uuid,
                ),
            )

    @fixtures.db.tenant()
    @fixtures.db.policy(name='foobar')
    def test_that_two_policies_cannot_have_the_same_name_and_tenant(
        self, tenant_uuid, policy_uuid
    ):
        # Same name different tenants no exception
        assert_that(
            calling(self.create_and_delete_policy).with_args(
                'foobar', tenant_uuid=tenant_uuid
            ),
            not_(raises(exceptions.DuplicatePolicyException)),
        )

        # Same tenant different names no exception
        assert_that(
            calling(self.create_and_delete_policy).with_args('foobaz'),
            not_(raises(exceptions.DuplicatePolicyException)),
        )

        # Same name same tenant
        assert_that(
            calling(self.create_and_delete_policy).with_args('foobar'),
            raises(exceptions.DuplicatePolicyException),
        )

    @fixtures.db.tenant()
    @fixtures.db.policy(slug='foobar')
    def test_that_two_policies_cannot_have_the_same_slug_and_tenant(
        self, tenant_uuid, policy_uuid
    ):
        # Same slug different tenants no exception
        assert_that(
            calling(self.create_and_delete_policy).with_args(
                'foobar', slug='foobar', tenant_uuid=tenant_uuid
            ),
            not_(raises(exceptions.DuplicatePolicyException)),
        )

        # Same tenant different slug no exception
        assert_that(
            calling(self.create_and_delete_policy).with_args('foobaz', slug='foobaz'),
            not_(raises(exceptions.DuplicatePolicyException)),
        )

        # Same name same tenant
        assert_that(
            calling(self.create_and_delete_policy).with_args('foobar', slug='foobar'),
            raises(exceptions.DuplicatePolicyException),
        )

        # Same name case insensitive same tenant
        assert_that(
            calling(self.create_and_delete_policy).with_args('fooBAR', slug='fooBAR'),
            raises(exceptions.DuplicatePolicyException),
        )

    def test_tenant_creation_auto_generates_slug(self):
        name = 'policy-name'
        with self._new_policy(name=name, slug=None) as policy_uuid:
            policy = self._policy_dao.find_by(uuid=policy_uuid)
            assert_that(policy, has_properties(slug=name))

    @fixtures.db.policy(name='foobar')
    def test_list(self, uuid_):
        policy = self._policy_dao.find_by(uuid=uuid_)
        assert_that(
            policy,
            has_properties(uuid=uuid_, name='foobar', description='', acl=empty()),
        )

        result = self._policy_dao.list_(uuid=UNKNOWN_UUID)
        assert_that(result, empty())

    @fixtures.db.policy(name='a', description='z')
    @fixtures.db.policy(name='b', description='y')
    @fixtures.db.policy(name='c', description='x')
    def test_list_sort_and_pagination(self, a, b, c):
        result = self.list_policy(order='name', direction='asc')
        assert_that(
            result,
            contains_exactly(
                a,
                b,
                c,
                self._default_master_user_policy_uuid,
            ),
        )

        result = self.list_policy(order='name', direction='desc')
        assert_that(
            result,
            contains_exactly(
                self._default_master_user_policy_uuid,
                c,
                b,
                a,
            ),
        )

        result = self.list_policy(order='description', direction='asc')
        assert_that(
            result,
            contains_exactly(
                self._default_master_user_policy_uuid,
                c,
                b,
                a,
            ),
        )

        result = self.list_policy(order='description', direction='desc')
        assert_that(
            result,
            contains_exactly(
                a,
                b,
                c,
                self._default_master_user_policy_uuid,
            ),
        )

        assert_that(
            calling(self.list_policy).with_args(order='foobar', direction='asc'),
            raises(exceptions.InvalidSortColumnException),
        )

        assert_that(
            calling(self.list_policy).with_args(order='name', direction='down'),
            raises(exceptions.InvalidSortDirectionException),
        )

        result = self.list_policy(order='name', direction='asc', limit=2)
        assert_that(result, contains_exactly(a, b))

        result = self.list_policy(order='name', direction='asc', offset=1)
        assert_that(
            result,
            contains_exactly(
                b,
                c,
                self._default_master_user_policy_uuid,
            ),
        )

        invalid_offsets = [-1, 'two', True, False]
        for offset in invalid_offsets:
            assert_that(
                calling(self.list_policy).with_args(
                    order='name', direction='asc', offset=offset
                ),
                raises(exceptions.InvalidOffsetException),
                offset,
            )

        invalid_limits = [-1, 'two', True, False]
        for limit in invalid_limits:
            assert_that(
                calling(self.list_policy).with_args(
                    order='name', direction='asc', limit=limit
                ),
                raises(exceptions.InvalidLimitException),
                limit,
            )

    @fixtures.db.policy(config_managed=True)
    @fixtures.db.policy(config_managed=False)
    def test_list_by_read_only(self, policy_1, policy_2):
        result = self._policy_dao.list_(read_only=True)
        assert_that(result, contains_exactly(has_properties(uuid=policy_1)))

        result = self._policy_dao.list_(read_only=False)
        assert_that(
            result,
            contains_inanyorder(
                has_properties(uuid=policy_2),
                has_properties(uuid=self._default_master_user_policy_uuid),
            ),
        )

        result = self._policy_dao.list_()
        assert_that(
            result,
            contains_inanyorder(
                has_properties(uuid=policy_1),
                has_properties(uuid=policy_2),
                has_properties(uuid=self._default_master_user_policy_uuid),
            ),
        )

    @fixtures.db.user()
    @fixtures.db.user()
    @fixtures.db.policy(name='name1', acl=['1', '2'])
    @fixtures.db.policy(name='name2', acl=['3', '4'])
    def test_list_policy_associated_to_multiple_users_appears_once(
        self, user_1, user_2, policy_1, policy_2
    ):
        self._user_dao.add_policy(user_1, policy_1)
        self._user_dao.add_policy(user_2, policy_1)

        result = self._policy_dao.list_(search='name', limit=2)
        assert_that(
            result,
            contains_inanyorder(
                has_properties(uuid=policy_1),
                has_properties(uuid=policy_2),
            ),
        )

    # fmt: off
    @fixtures.db.tenant(name='top', uuid=TENANT_UUID_1)
    @fixtures.db.tenant(name='child', uuid=TENANT_UUID_2, parent_uuid=TENANT_UUID_1)
    @fixtures.db.tenant(name='hidden', uuid=TENANT_UUID_3, parent_uuid=TENANT_UUID_1)
    @fixtures.db.tenant(name='child-hidden', uuid=TENANT_UUID_4, parent_uuid=TENANT_UUID_2)
    @fixtures.db.policy(slug='top-shared', tenant_uuid=TENANT_UUID_1, shared=True)
    @fixtures.db.policy(slug='child-normal', tenant_uuid=TENANT_UUID_2)
    @fixtures.db.policy(slug='hidden-shared', tenant_uuid=TENANT_UUID_3, shared=True)
    @fixtures.db.policy(slug='child-hidden-shared', tenant_uuid=TENANT_UUID_4, shared=True)
    # fmt: on
    def test_methods_with_shared(self, *_):
        expected = [
            has_properties(
                slug='top-shared',
                read_only=True,
                tenant_uuid_exposed=TENANT_UUID_2,
            ),
            has_properties(
                slug='child-normal',
                read_only=False,
                tenant_uuid_exposed=TENANT_UUID_2,
            ),
        ]

        result = self._policy_dao.list_(tenant_uuids=[TENANT_UUID_2])
        assert_that(result, contains_inanyorder(*expected))

        result = self._policy_dao.count(search=None, tenant_uuids=[TENANT_UUID_2])
        assert_that(result, equal_to(len(expected)))

    @fixtures.db.user()
    @fixtures.db.policy(name='a')
    @fixtures.db.policy(name='b', description='The second foobar')
    @fixtures.db.policy(name='c', description='The third foobar')
    def test_user_list_policies(self, user_uuid, policy_a, policy_b, policy_c):
        result = self._policy_dao.list_(user_uuid=user_uuid)
        assert_that(result, empty(), 'empty')

        self._user_dao.add_policy(user_uuid, policy_a)
        self._user_dao.add_policy(user_uuid, policy_b)
        self._user_dao.add_policy(user_uuid, policy_c)

        result = self._policy_dao.list_(user_uuid=user_uuid)
        assert_that(
            result,
            contains_inanyorder(
                has_properties(name='a'),
                has_properties(name='b'),
                has_properties(name='c'),
            ),
        )

    @fixtures.db.policy()
    def test_delete(self, uuid):
        assert_that(
            calling(self._policy_dao.delete).with_args(uuid, [self.top_tenant_uuid]),
            not_(raises(Exception)),
        )

        assert_that(
            calling(self._policy_dao.delete).with_args(
                UNKNOWN_UUID, [self.top_tenant_uuid]
            ),
            raises(exceptions.UnknownPolicyException),
        )

    def test_update(self):
        assert_that(
            calling(self._policy_dao.update).with_args(
                UNKNOWN_UUID, 'foo', '', [], False
            ),
            raises(exceptions.UnknownPolicyException),
        )

        body = {
            'name': 'foobar',
            'slug': 'foobar',
            'description': 'description',
            'acl': ['dird.#'],
        }
        with self._new_policy(**body) as uuid_:
            self._policy_dao.update(
                uuid_,
                'foobaz',
                'A new description',
                ['dird.#', 'ctid-ng.#'],
                False,
            )
            policy = self._policy_dao.find_by(uuid=uuid_)

            assert_that(
                policy,
                has_properties(
                    uuid=uuid_,
                    name='foobaz',
                    description='A new description',
                    acl=contains_inanyorder('dird.#', 'ctid-ng.#'),
                ),
            )

    @fixtures.db.user()
    @fixtures.db.policy()
    def test_is_associated_user(self, user_uuid, policy_uuid):
        result = self._policy_dao._is_associated_user(policy_uuid)
        assert_that(result, equal_to(False))

        self._user_dao.add_policy(user_uuid, policy_uuid)
        result = self._policy_dao._is_associated_user(policy_uuid)
        assert_that(result, equal_to(True))

    @fixtures.db.group()
    @fixtures.db.policy()
    def test_is_associated_group(self, group_uuid, policy_uuid):
        result = self._policy_dao._is_associated_group(policy_uuid)
        assert_that(result, equal_to(False))

        self._group_dao.add_policy(group_uuid, policy_uuid)
        result = self._policy_dao._is_associated_group(policy_uuid)
        assert_that(result, equal_to(True))

    @fixtures.db.user()
    @fixtures.db.group()
    @fixtures.db.policy()
    def test_is_associated(self, user_uuid, group_uuid, policy_uuid):
        # without user, without group
        result = self._policy_dao.is_associated(policy_uuid)
        assert_that(result, equal_to(False))

        # without user, with group
        self._group_dao.add_policy(group_uuid, policy_uuid)
        result = self._policy_dao.is_associated(policy_uuid)
        assert_that(result, equal_to(True))

        # with user, with group
        self._user_dao.add_policy(user_uuid, policy_uuid)
        result = self._policy_dao.is_associated(policy_uuid)
        assert_that(result, equal_to(True))

        # with user, without group
        self._group_dao.remove_policy(group_uuid, policy_uuid)
        result = self._policy_dao.is_associated(policy_uuid)
        assert_that(result, equal_to(True))

    def list_policy(self, order=None, direction=None, limit=None, offset=None):
        policies = self._policy_dao.list_(
            order=order,
            direction=direction,
            limit=limit,
            offset=offset,
        )
        return [policy.uuid for policy in policies]

    @fixtures.db.tenant()
    @fixtures.db.policy()
    def test_get(self, tenant_uuid, policy_uuid):
        policy = self._policy_dao.get(policy_uuid)
        assert_that(policy.uuid, equal_to(policy_uuid))

        assert_that(
            calling(self._policy_dao.get).with_args(UNKNOWN_UUID),
            raises(exceptions.UnknownPolicyException),
        )

        policy = self._policy_dao.get(policy_uuid, tenant_uuids=[self.top_tenant_uuid])
        assert_that(policy.uuid, equal_to(policy_uuid))

        assert_that(
            calling(self._policy_dao.get).with_args(
                policy_uuid,
                tenant_uuids=[tenant_uuid],
            ),
            raises(exceptions.UnknownPolicyException),
        )

    @fixtures.db.tenant()
    @fixtures.db.policy(slug='slug')
    def test_get_by(self, tenant_uuid, policy_uuid):
        policy = self._policy_dao.get_by(slug='slug')
        assert_that(policy.uuid, equal_to(policy_uuid))

        assert_that(
            calling(self._policy_dao.get).with_args(UNKNOWN_SLUG),
            raises(exceptions.UnknownPolicyException),
        )

    @contextmanager
    def _new_policy(
        self, name, slug=None, description=None, acl=None, tenant_uuid=None
    ):
        tenant_uuid = tenant_uuid or self.top_tenant_uuid
        acl = acl or []
        slug = slug or name
        uuid_ = self._policy_dao.create(
            name=name,
            slug=slug,
            description=description,
            acl=acl,
            tenant_uuid=tenant_uuid,
            config_managed=False,
            shared=False,
        )
        try:
            yield uuid_
        finally:
            self._policy_dao.delete(uuid_, [tenant_uuid])

    def create_and_delete_policy(self, *args, **kwargs):
        with self._new_policy(*args, **kwargs):
            pass
