# Copyright 2023 Accent Communications


class RetentionService:
    def __init__(self, dao, notifier):
        self._dao = dao
        self._notifier = notifier

    def find(self, tenant_uuid):
        return self._dao.retention.find(tenant_uuid)

    def find_or_create(self, tenant_uuid):
        return self._dao.retention.find_or_create(tenant_uuid)

    def update(self, retention):
        self._dao.retention.update(retention)
        self._notifier.updated(retention)
