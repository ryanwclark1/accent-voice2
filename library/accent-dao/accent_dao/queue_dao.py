# Copyright 2023 Accent Communications

from accent_dao.alchemy.queuefeatures import QueueFeatures
from accent_dao.helpers.db_manager import daosession


@daosession
def get(session, queue_id, tenant_uuids=None):
    query = session.query(QueueFeatures).filter(QueueFeatures.id == queue_id)

    if tenant_uuids is not None:
        query = query.filter(QueueFeatures.tenant_uuid.in_(tenant_uuids))

    result = query.first()
    if result is None:
        raise LookupError('No such queue')
    else:
        return result
