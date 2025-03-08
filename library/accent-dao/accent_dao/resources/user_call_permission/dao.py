# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import Session
from accent_dao.resources.user_call_permission.persistor import Persistor


def persistor():
    return Persistor(Session)


def get_by(**criteria):
    return persistor().get_by(**criteria)


def find_by(**criteria):
    return persistor().find_by(**criteria)


def find_all_by(**criteria):
    return persistor().find_all_by(**criteria)


def associate(user, call_permission):
    return persistor().associate_user_call_permission(user, call_permission)


def dissociate(user, call_permission):
    return persistor().dissociate_user_call_permission(user, call_permission)


def dissociate_all_by_user(user):
    return persistor().dissociate_all_call_permissions_by_user(user)
