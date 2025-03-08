# Copyright 2023 Accent Communications

from accent_dao.helpers import errors
from accent_dao.helpers.exception import NotFoundError
from accent_dao.resources.group import dao as group_dao
from accent_dao.resources.user import dao as user_dao

from accent_confd.plugins.user_group.resource import GroupsIDUUIDSchema


class UserGroupAssociationMiddleWare:
    def __init__(self, service):
        self._service = service
        self._schema = GroupsIDUUIDSchema()

    def associate_all_groups(self, body, user_id):
        form = self._schema.load(body)
        try:
            groups = [group_dao.get_by(**group) for group in form['groups']]
        except NotFoundError as e:
            raise errors.param_not_found('groups', 'Group', **e.metadata)

        self._service.associate_all_groups(
            user_dao.get_by_id_uuid(user_id),
            groups,
        )
