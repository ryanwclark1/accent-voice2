# Copyright 2023 Accent Communications

from accent_dao.resources.call_filter import dao as call_filter_dao
from accent_dao.resources.user import dao as user_dao

from .resource import CallFilterRecipientUserList, CallFilterSurrogateUserList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            CallFilterRecipientUserList,
            '/callfilters/<int:call_filter_id>/recipients/users',
            endpoint='call_filter_recipients_users',
            resource_class_args=(service, call_filter_dao, user_dao),
        )

        api.add_resource(
            CallFilterSurrogateUserList,
            '/callfilters/<int:call_filter_id>/surrogates/users',
            endpoint='call_filter_surrogate_users',
            resource_class_args=(service, call_filter_dao, user_dao),
        )
