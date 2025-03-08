# Copyright 2023 Accent Communications

import abc
import logging
import os

DEFAULT_ACCENT_UUID = os.getenv('ACCENT_UUID')
logger = logging.getLogger(__name__)


class BaseAuthenticationBackend(metaclass=abc.ABCMeta):
    def __init__(self):
        """Initialize this backend instance from the given configuration"""
        pass

    def load(self, dependencies):
        pass

    def get_acl(self, login, args):
        """returns an acl"""
        return []

    def get_accent_uuid(self, _args):
        """returns the accent-uuid for this given backend

        Will return the ACCENT_UUID environment variable if the backend does not implement
        this method.
        """
        return DEFAULT_ACCENT_UUID

    def get_metadata(self, login, args):
        """return user related data

        these data are used in the body of the GET and POST of the /token
        """
        metadata = {
            'auth_id': None,
            'username': login,
            'accent_uuid': self.get_accent_uuid(args),
            'pbx_user_uuid': None,
        }

        return metadata

    @abc.abstractmethod
    def verify_password(self, login, passwd, args):
        """Checks if a login/password combination is correct, returns True or False.

        It's possible to pass values through the args parameter. These values
        will be passed to the other methods of the plugin.
        """


class BaseMetadata(metaclass=abc.ABCMeta):
    def __init__(self):
        """Initialize this plugin instance from the given configuration"""
        pass

    def load(self, dependencies):
        self._user_service = dependencies['user_service']

    def get_token_metadata(self, login, args):
        """return user related data

        These data are used in the body of the GET and POST of the /token
        """
        user_uuid = self._user_service.get_user_uuid_by_login(login)
        user = self._user_service.list_users(uuid=user_uuid)[0]
        metadata = {
            'uuid': user['uuid'],
            'tenant_uuid': user['tenant_uuid'],
            'auth_id': user['uuid'],
            'pbx_user_uuid': None,
            'accent_uuid': self.get_accent_uuid(args),
        }
        return metadata

    def get_accent_uuid(self, _args):
        """returns the accent-uuid for this given backend

        Will return the ACCENT_UUID environment variable if the backend does not implement
        this method.
        """
        return DEFAULT_ACCENT_UUID
