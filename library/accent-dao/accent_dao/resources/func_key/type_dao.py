# Copyright 2023 Accent Communications

from accent_dao.alchemy.func_key_destination_type import (
    FuncKeyDestinationType as FuncKeyDestinationTypeSchema,
)
from accent_dao.alchemy.func_key_type import FuncKeyType as FuncKeyTypeSchema
from accent_dao.helpers.db_manager import daosession


@daosession
def find_type_for_name(session, name):
    return _find_using_name(session, FuncKeyTypeSchema, name)


@daosession
def find_destination_type_for_name(session, name):
    return _find_using_name(session, FuncKeyDestinationTypeSchema, name)


def _find_using_name(session, schema, name):
    return session.query(schema).filter(schema.name == name).first()
