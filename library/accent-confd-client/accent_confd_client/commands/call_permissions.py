# Copyright 2023 Accent Communications

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import UserCallPermissionRelation
from accent_confd_client.util import extract_id


class CallPermissionRelation:
    def __init__(self, builder, call_permission_id):
        self.call_permission_id = call_permission_id
        self.user_call_permission = UserCallPermissionRelation(builder)

    @extract_id
    def add_user(self, user_id):
        return self.user_call_permission.associate(user_id, self.call_permission_id)

    @extract_id
    def remove_user(self, user_id):
        return self.user_call_permission.dissociate(user_id, self.call_permission_id)


class CallPermissionsCommand(MultiTenantCommand):
    resource = 'callpermissions'
    relation_cmd = CallPermissionRelation
