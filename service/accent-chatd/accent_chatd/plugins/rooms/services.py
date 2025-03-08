# Copyright 2023 Accent Communications


class RoomService:
    def __init__(self, accent_uuid, dao, notifier):
        self._dao = dao
        self._notifier = notifier
        self._accent_uuid = accent_uuid

    def create(self, room):
        self._set_default_room_values(room)
        self._dao.room.create(room)
        self._notifier.created(room)
        return room

    def _set_default_room_values(self, room):
        for user in room.users:
            if user.tenant_uuid is None:
                user.tenant_uuid = room.tenant_uuid
            if user.accent_uuid is None:
                user.accent_uuid = self._accent_uuid

    def list_(self, tenant_uuids, **filter_parameters):
        return self._dao.room.list_(tenant_uuids, **filter_parameters)

    def count(self, tenant_uuids, **filter_parameters):
        return self._dao.room.count(tenant_uuids, **filter_parameters)

    def get(self, tenant_uuids, room_uuid):
        return self._dao.room.get(tenant_uuids, room_uuid)

    def create_message(self, room, message):
        self._set_default_message_values(message)
        self._dao.room.add_message(room, message)
        self._notifier.message_created(room, message)
        return message

    def _set_default_message_values(self, message):
        message.accent_uuid = self._accent_uuid

    def list_messages(self, room, **filter_parameters):
        return self._dao.room.list_messages(room, **filter_parameters)

    def count_messages(self, room, **filter_parameters):
        return self._dao.room.count_messages(room, **filter_parameters)

    def list_user_messages(self, tenant_uuid, user_uuid, **filter_parameters):
        return self._dao.room.list_user_messages(
            tenant_uuid, user_uuid, **filter_parameters
        )

    def count_user_messages(self, tenant_uuid, user_uuid, **filter_parameters):
        return self._dao.room.count_user_messages(
            tenant_uuid, user_uuid, **filter_parameters
        )
