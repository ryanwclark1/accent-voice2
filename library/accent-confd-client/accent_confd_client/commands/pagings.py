# Copyright 2023 Accent Communications

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import (
    PagingCallerUserRelation,
    PagingMemberUserRelation,
)


class PagingRelation:
    def __init__(self, builder, paging_id):
        self.paging_id = paging_id
        self.paging_user_callers = PagingCallerUserRelation(builder)
        self.paging_user_members = PagingMemberUserRelation(builder)

    def update_user_members(self, users):
        return self.paging_user_members.associate(self.paging_id, users)

    def update_user_callers(self, users):
        return self.paging_user_callers.associate(self.paging_id, users)


class PagingsCommand(MultiTenantCommand):
    resource = 'pagings'
    relation_cmd = PagingRelation
