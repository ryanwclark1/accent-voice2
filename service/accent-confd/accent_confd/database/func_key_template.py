# Copyright 2023 Accent Communications

from accent_dao.alchemy.func_key import FuncKey
from accent_dao.alchemy.func_key_dest_user import FuncKeyDestUser
from accent_dao.alchemy.func_key_mapping import FuncKeyMapping
from accent_dao.alchemy.func_key_template import FuncKeyTemplate
from accent_dao.helpers.db_manager import Session


def find_all_dst_user(user_id):
    query = (
        Session.query(FuncKeyTemplate)
        .join(FuncKeyMapping, FuncKeyTemplate.id == FuncKeyMapping.template_id)
        .join(FuncKey, FuncKeyMapping.func_key_id == FuncKey.id)
        .join(FuncKeyDestUser, FuncKey.id == FuncKeyDestUser.func_key_id)
        .filter(FuncKeyDestUser.user_id == user_id)
    )

    return query.all()
