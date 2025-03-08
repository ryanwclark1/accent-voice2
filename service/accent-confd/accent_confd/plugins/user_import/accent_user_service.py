# Copyright 2023 Accent Communications

from .auth_client import auth_client


class AccentUserService:
    def __init__(self, auth_client):
        self._auth_client = auth_client

    def create(self, user):
        return self._auth_client.new_user(
            uuid=user.get('uuid'),
            firstname=user.get('firstname'),
            lastname=user.get('lastname'),
            email_address=user.get('email_address'),
            username=user.get('username')
            or user.get('email_address')
            or user.get('uuid'),
            password=user.get('password'),
            enabled=user.get('enabled') if user.get('enabled') is not None else True,
            tenant_uuid=user.get('tenant_uuid'),
        )

    def update(self, user):
        self._auth_client.edit_user(user['uuid'], **user)
        self._auth_client.admin.update_user_emails(user['uuid'], user['emails'])
        if user.get('password'):
            self._auth_client.users.set_password(user['uuid'], user['password'])

    def delete(self, uuid):
        self._auth_client.delete(uuid)

    def get(self, uuid):
        self._auth_client.get(uuid)


def build_service():
    return AccentUserService(auth_client)
