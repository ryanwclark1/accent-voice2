# Copyright 2023 Accent Communications

import datetime
import logging
import os

from sqlalchemy import func

from .database.models import CallLog, Config, Export, Recording, Retention, Tenant

logger = logging.getLogger(__name__)

DEFAULT_PURGE_DB_DAYS = 365
DEFAULT_CALL_LOGD_CDR_DAYS = 365
DEFAULT_CALL_LOGD_RECORDING_DAYS = 365
DEFAULT_CALL_LOGD_EXPORT_DAYS = 2


def _remove_export_files(exports):
    for export in exports:
        if not export.path:
            logger.debug('Export file never created: "%s"', export.uuid)
            continue

        try:
            os.remove(export.path)
        except FileNotFoundError:
            logger.info('Export file already deleted: "%s"', export.path)


def _remove_recording_files(call_logs):
    for call_log in call_logs:
        for recording in call_log.recordings:
            if recording.path:
                logger.debug('Deleting recording file %s', recording.path)
                try:
                    # NOTE: accent-purge-db must be executed
                    # on the same filesystem than accent-call-logd
                    os.remove(recording.path)
                except FileNotFoundError:
                    logger.info('Recording file already deleted: "%s"', recording.path)


def _extract_days_to_keep(tenant_days, default_days, purge_db_days, default):
    if tenant_days is not None:
        return tenant_days

    purge_db_days_customized = purge_db_days != DEFAULT_PURGE_DB_DAYS
    default_days_customized = default_days != default
    if purge_db_days_customized and not default_days_customized:
        return purge_db_days

    return default_days


def _get_tenants_uuids(session, tenant_uuid):
    if tenant_uuid:
        return [tenant_uuid]
    else:
        return [tenant_uuid[0] for tenant_uuid in session.query(Tenant.uuid).all()]


class CallLogsPurger:
    def purge(self, days_to_keep, session, tenant_uuid=None):
        config = session.query(Config).first()
        if not config:
            raise Exception('No default config found')
        default_days = config.retention_cdr_days

        retentions = {r.tenant_uuid: r for r in session.query(Retention).all()}
        tenants_uuid = _get_tenants_uuids(session, tenant_uuid)
        for tenant_uuid in tenants_uuid:
            retention = retentions.get(tenant_uuid)
            tenant_days = retention.cdr_days if retention else None
            days = _extract_days_to_keep(
                tenant_days,
                default_days,
                days_to_keep,
                DEFAULT_CALL_LOGD_CDR_DAYS,
            )
            if days != days_to_keep:
                logger.debug(
                    'Tenant %s: overriding call log retention to %s days',
                    tenant_uuid,
                    days,
                )

            max_date = func.now() - datetime.timedelta(days=days)
            query = (
                session.query(CallLog)
                .join(Recording, Recording.call_log_id == CallLog.id)
                .filter(CallLog.date < max_date)
                .filter(CallLog.tenant_uuid == tenant_uuid)
            )
            call_logs = query.all()
            _remove_recording_files(call_logs)

            query = (
                session.query(CallLog)
                .filter(CallLog.date < max_date)
                .filter(CallLog.tenant_uuid == tenant_uuid)
            )
            query.delete(synchronize_session=False)


class ExportsPurger:
    def purge(self, days_to_keep, session, tenant_uuid=None):
        config = session.query(Config).first()
        if not config:
            raise Exception('No default config found')
        default_days = config.retention_export_days

        retentions = {r.tenant_uuid: r for r in session.query(Retention).all()}
        tenants_uuid = _get_tenants_uuids(session, tenant_uuid)
        for tenant_uuid in tenants_uuid:
            days = days_to_keep
            retention = retentions.get(tenant_uuid)
            tenant_days = retention.export_days if retention else None
            days = _extract_days_to_keep(
                tenant_days,
                default_days,
                days_to_keep,
                DEFAULT_CALL_LOGD_EXPORT_DAYS,
            )
            if days != days_to_keep:
                logger.debug(
                    'Tenant %s: overriding export retention to %s days',
                    tenant_uuid,
                    days,
                )

            max_date = func.now() - datetime.timedelta(days=days)
            query = (
                session.query(Export)
                .filter(Export.requested_at < max_date)
                .filter(Export.tenant_uuid == tenant_uuid)
            )
            exports = query.all()
            _remove_export_files(exports)

            query.delete(synchronize_session=False)


class RecordingsPurger:
    def purge(self, days_to_keep, session, tenant_uuid=None):
        config = session.query(Config).first()
        if not config:
            raise Exception('No default config found')
        default_days = config.retention_recording_days

        retentions = {r.tenant_uuid: r for r in session.query(Retention).all()}
        tenants_uuid = _get_tenants_uuids(session, tenant_uuid)
        for tenant_uuid in tenants_uuid:
            days = days_to_keep
            retention = retentions.get(tenant_uuid)
            tenant_days = retention.recording_days if retention else None
            days = _extract_days_to_keep(
                tenant_days,
                default_days,
                days_to_keep,
                DEFAULT_CALL_LOGD_RECORDING_DAYS,
            )
            if days != days_to_keep:
                logger.debug(
                    'Tenant %s: overriding recording retention to %s days',
                    tenant_uuid,
                    days,
                )

            max_date = func.now() - datetime.timedelta(days=days)
            query = (
                session.query(CallLog)
                .join(Recording, Recording.call_log_id == CallLog.id)
                .filter(CallLog.date < max_date)
                .filter(CallLog.tenant_uuid == tenant_uuid)
            )
            call_logs = query.all()
            _remove_recording_files(call_logs)

            subquery = (
                session.query(CallLog.id)
                .filter(CallLog.date < max_date)
                .filter(CallLog.tenant_uuid == tenant_uuid)
            )
            query = session.query(Recording).filter(Recording.call_log_id.in_(subquery))
            query.update({'path': None}, synchronize_session=False)
