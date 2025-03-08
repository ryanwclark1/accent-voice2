# Copyright 2023 Accent Communications

from accent_dao.resources.meeting import dao as meeting_dao
from accent_dao.resources.meeting_authorization import dao as meeting_authorization_dao

from accent_confd import bus

from .notifier import Notifier
from .resource import (
    GuestMeetingAuthorizationItem,
    GuestMeetingAuthorizationList,
    UserMeetingAuthorizationAccept,
    UserMeetingAuthorizationItem,
    UserMeetingAuthorizationList,
    UserMeetingAuthorizationReject,
)
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        api_notifier = Notifier(bus)
        service = build_service(api_notifier)

        api.add_resource(
            GuestMeetingAuthorizationList,
            '/guests/<guest_uuid>/meetings/<uuid:meeting_uuid>/authorizations',
            endpoint='guest_meeting_authorization_list',
            resource_class_args=[service, meeting_dao],
        )

        api.add_resource(
            GuestMeetingAuthorizationItem,
            '/guests/<guest_uuid>/meetings/<uuid:meeting_uuid>/authorizations/<uuid:authorization_uuid>',
            endpoint='guest_meeting_authorization',
            resource_class_args=[service, meeting_dao],
        )

        api.add_resource(
            UserMeetingAuthorizationList,
            '/users/me/meetings/<uuid:meeting_uuid>/authorizations',
            endpoint='user_meeting_authorization_list',
            resource_class_args=[service, meeting_dao],
        )

        api.add_resource(
            UserMeetingAuthorizationItem,
            '/users/me/meetings/<uuid:meeting_uuid>/authorizations/<uuid:authorization_uuid>',
            endpoint='user_meeting_authorization',
            resource_class_args=[service, meeting_authorization_dao],
        )

        api.add_resource(
            UserMeetingAuthorizationAccept,
            '/users/me/meetings/<uuid:meeting_uuid>/authorizations/<uuid:authorization_uuid>/accept',
            endpoint='user_meeting_authorization_accept',
            resource_class_args=[service, meeting_authorization_dao],
        )

        api.add_resource(
            UserMeetingAuthorizationReject,
            '/users/me/meetings/<uuid:meeting_uuid>/authorizations/<uuid:authorization_uuid>/reject',
            endpoint='user_meeting_authorization_reject',
            resource_class_args=[service, meeting_authorization_dao],
        )
