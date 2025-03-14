# Copyright 2023 Accent Communications

from flask import request

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource

from .schema import UserFallbackSchema


class UserFallbackList(ConfdResource):
    schema = UserFallbackSchema

    def __init__(self, service, user_dao, user_fallback_middleware):
        super().__init__()
        self.service = service
        self.user_dao = user_dao
        self._user_fallback_middleware = user_fallback_middleware

    @required_acl('confd.users.{user_id}.fallbacks.read')
    def get(self, user_id):
        return self._user_fallback_middleware.get(user_id)

    @required_acl('confd.users.{user_id}.fallbacks.update')
    def put(self, user_id):
        self._user_fallback_middleware.associate(user_id, request.get_json())
        return '', 204
