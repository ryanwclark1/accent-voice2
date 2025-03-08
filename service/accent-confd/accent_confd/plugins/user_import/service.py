# Copyright 2023 Accent Communications

import logging

from accent_dao import tenant_dao
from accent_dao.helpers.exception import ServiceError
from marshmallow import ValidationError

logger = logging.getLogger(__name__)


class ImportService:
    def __init__(self, entry_creator, entry_associator, entry_updater):
        self.entry_creator = entry_creator
        self.entry_associator = entry_associator
        self.entry_updater = entry_updater

    def import_rows(self, parser, tenant_uuid):
        tenant_dao.find_or_create_tenant(tenant_uuid)
        created = []
        errors = []

        for row in parser:
            try:
                entry = self.create_entry(row, tenant_uuid)
                created.append(entry)
            except (ServiceError, ValidationError) as e:
                logger.warn("Error importing CSV row %s: %s", row.position, e)
                errors.append(row.format_error(e))

        return created, errors

    def create_entry(self, row, tenant_uuid):
        entry = self.entry_creator.create(row, tenant_uuid=tenant_uuid)
        self.entry_associator.associate(entry)
        return entry

    def update_rows(self, parser, tenant_uuid):
        updated = []
        errors = []

        for row in parser:
            try:
                entry = self.update_row(row, tenant_uuid)
                updated.append(entry)
            except (ServiceError, ValidationError) as e:
                logger.warn("ERROR importing CSV row %s: %s", row.position, e)
                errors.append(row.format_error(e))

        return updated, errors

    def update_row(self, row, tenant_uuid):
        entry = self.entry_updater.update_row(row, tenant_uuid)
        return entry


class ExportService:
    def __init__(self, user_export_dao, auth_client):
        self._user_export_dao = user_export_dao
        self._auth_client = auth_client

    def export(self, tenant_uuid):
        csv_header, users = self._user_export_dao.export_query(tenant_uuid)
        users = list(self._format_users(csv_header, users))

        accent_users = self._auth_client.users.list(tenant_uuid=tenant_uuid)['items']
        accent_users = {user['uuid']: user for user in accent_users}
        for user in users:
            if user['uuid'] in accent_users:
                accent_user = accent_users[user['uuid']]
                user['username'] = accent_user['username']
            else:
                logger.warning(
                    "User '%s' has no accent-auth user associated. Please create one with same uuid",
                    user['uuid'],
                )

        csv_header = csv_header + ('username',)

        return csv_header, users

    def _format_users(self, header, users):
        for user in users:
            user_row = tuple((field or "") for field in user)
            user_dict = dict(zip(header, user_row))
            yield user_dict
