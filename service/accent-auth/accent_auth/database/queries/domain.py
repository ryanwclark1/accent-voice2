# Copyright 2023 Accent Communications

from ..models import Domain
from .base import BaseDAO


class DomainDAO(BaseDAO):
    def list(self, tenant_uuid=None) -> list[Domain]:
        if tenant_uuid:
            return (
                self.session.query(Domain)
                .filter(Domain.tenant_uuid == tenant_uuid)
                .all()
            )
        else:
            return self.session.query(Domain).all()

    def get(self, tenant_uuid):
        return (
            self.session.query(Domain).filter(Domain.tenant_uuid == tenant_uuid).all()
        )
