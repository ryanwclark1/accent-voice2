# Copyright 2023 Accent Communications

from accent_auth import exceptions

from ..models import Email
from .base import BaseDAO


class EmailDAO(BaseDAO):
    def confirm(self, email_uuid):
        filter_ = Email.uuid == str(email_uuid)
        nb_updated = (
            self.session.query(Email).filter(filter_).update({'confirmed': True})
        )
        self.session.flush()

        if not nb_updated:
            raise exceptions.UnknownEmailException(email_uuid)
