# Copyright 2023 Accent Communications

from accent_dao.resources.moh import dao as moh_dao

from accent_confd.helpers.validator import MOHExists, ValidationGroup


def build_validator():
    moh_validator = MOHExists('music_on_hold', moh_dao.get_by)
    return ValidationGroup(create=[moh_validator], edit=[moh_validator])
