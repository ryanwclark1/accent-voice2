# Copyright 2023 Accent Communications

import uuid

from accent_test_helpers.hamcrest.raises import raises
from hamcrest import assert_that, calling, equal_to

from accent_auth import exceptions
from accent_auth.database import models

from .helpers import base, fixtures
from .helpers.constants import UNKNOWN_UUID

SESSION_UUID_1 = str(uuid.uuid4())


@base.use_asset('database')
class TestEmailDAO(base.DAOTestCase):
    @fixtures.db.email()
    def test_confirm(self, email_uuid):
        assert_that(self.is_email_confirmed(email_uuid), equal_to(False))
        assert_that(
            calling(self._email_dao.confirm).with_args(UNKNOWN_UUID),
            raises(exceptions.UnknownEmailException),
        )
        self._email_dao.confirm(email_uuid)
        assert_that(self.is_email_confirmed(email_uuid), equal_to(True))

    def is_email_confirmed(self, email_uuid):
        emails = self.session.query(models.Email).filter(
            models.Email.uuid == str(email_uuid)
        )
        for email in emails.all():
            return email.confirmed
        return False
