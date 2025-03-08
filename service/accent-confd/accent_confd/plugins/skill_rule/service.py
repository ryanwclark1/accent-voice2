# Copyright 2023 Accent Communications

from accent_dao.resources.skill_rule import dao as skill_rule_dao

from accent_confd.helpers.resource import CRUDService

from .notifier import build_notifier
from .validator import build_validator


def build_service():
    return CRUDService(skill_rule_dao, build_validator(), build_notifier())
