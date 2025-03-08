# Copyright 2023 Accent Communications

from accent_auth import BaseAuthenticationBackend


class BrokenVerifyPasswordBackend(BaseAuthenticationBackend):
    def verify_password(self, login, password, args):
        return 0 / 1


class BrokenInitBackend(BaseAuthenticationBackend):
    def load(self, dependencies):
        super().load(dependencies)
        return dict()['foo']['bar']

    def verify_password(self, login, password, args):
        pass
