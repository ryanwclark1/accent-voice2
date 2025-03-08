# Copyright 2023 Accent Communications

from contextlib import contextmanager

from accent_dao.helpers.db_manager import Session
from accent_dao.resources.incall.persistor import IncallPersistor
from accent_dao.resources.incall.search import incall_search


def persistor(tenant_uuids=None):
    return IncallPersistor(Session, incall_search, tenant_uuids)


def search(tenant_uuids=None, **parameters):
    return persistor(tenant_uuids).search(parameters)


def get(incall_id, tenant_uuids=None):
    return persistor(tenant_uuids).get_by({'id': incall_id})


def get_by(tenant_uuids=None, **criteria):
    return persistor(tenant_uuids).get_by(criteria)


def find(incall_id, tenant_uuids=None):
    return persistor(tenant_uuids).find_by({'id': incall_id})


def find_by(tenant_uuids=None, **criteria):
    return persistor(tenant_uuids).find_by(criteria)


def find_all_by(tenant_uuids=None, **criteria):
    return persistor(tenant_uuids).find_all_by(criteria)


def find_main_callerid(tenant_uuid):
    return persistor().find_main_callerid(tenant_uuid)


def create(incall):
    return persistor().create(incall)


def edit(incall):
    persistor().edit(incall)


def delete(incall):
    persistor().delete(incall)


@contextmanager
def query_options(*options):
    with IncallPersistor.context_query_options(*options):
        yield
