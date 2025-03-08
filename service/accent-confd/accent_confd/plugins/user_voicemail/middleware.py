# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import Session
from accent_dao.resources.user import dao as user_dao
from accent_dao.resources.voicemail import dao as voicemail_dao


class UserVoicemailMiddleware:
    def __init__(self, service, middleware_handle):
        self._service = service
        self._middleware_handle = middleware_handle

    def associate(self, user_id, voicemail_id, tenant_uuids):
        user = user_dao.get_by_id_uuid(user_id, tenant_uuids=tenant_uuids)
        voicemail = voicemail_dao.get(voicemail_id, tenant_uuids=tenant_uuids)
        self._service.associate(user, voicemail)

    def create_voicemail(self, user_id, body, tenant_uuids):
        voicemail_middleware = self._middleware_handle.get('voicemail')
        voicemail = voicemail_middleware.create(body, tenant_uuids)
        self.associate(user_id, voicemail['id'], tenant_uuids)
        return voicemail

    def dissociate(self, user_id, tenant_uuids):
        user = user_dao.get_by_id_uuid(user_id, tenant_uuids=tenant_uuids)
        self._service.dissociate_all_by_user(user)

    def delete_voicemail(self, user_id, tenant_uuids):
        user = user_dao.get_by_id_uuid(user_id, tenant_uuids=tenant_uuids)
        voicemail_middleware = self._middleware_handle.get('voicemail')
        voicemail_id = user.voicemailid

        self.dissociate(user_id, tenant_uuids)
        Session.expire(user, ['voicemail'])

        voicemail = voicemail_middleware.get(voicemail_id, tenant_uuids)
        if not voicemail['users']:
            voicemail_middleware.delete(voicemail['id'], tenant_uuids)
