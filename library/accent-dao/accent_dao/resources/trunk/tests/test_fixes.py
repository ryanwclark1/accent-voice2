# Copyright 2023 Accent Communications


from hamcrest import assert_that, equal_to

from accent_dao.alchemy.useriax import UserIAX
from accent_dao.alchemy.usercustom import UserCustom
from accent_dao.resources.trunk.fixes import TrunkFixes
from accent_dao.tests.test_dao import DAOTestCase


class TestTrunkFixes(DAOTestCase):

    def setUp(self):
        super().setUp()
        self.fixes = TrunkFixes(self.session)

    def test_given_trunk_has_iax_endpoint_then_category_and_context_updated(self):
        iax = self.add_useriax(context=None, category='user')
        trunk = self.add_trunk(endpoint_iax_id=iax.id, context='mycontext')

        self.fixes.fix(trunk.id)

        iax = self.session.query(UserIAX).first()
        assert_that(iax.category, equal_to('trunk'))
        assert_that(iax.context, equal_to('mycontext'))

    def test_given_trunk_has_custom_endpoint_then_category_and_context_updated(self):
        custom = self.add_usercustom(context=None, category='user')
        trunk = self.add_trunk(endpoint_custom_id=custom.id, context='mycontext')

        self.fixes.fix(trunk.id)

        custom = self.session.query(UserCustom).first()
        assert_that(custom.category, equal_to('trunk'))
        assert_that(custom.context, equal_to('mycontext'))
