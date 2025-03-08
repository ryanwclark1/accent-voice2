# Copyright 2023 Accent Communications

from accent_dao.helpers import errors
from accent_dao.resources.moh import dao as moh_dao
from accent_dao.resources.user import dao as user_dao

from accent_confd.helpers.validator import (
    MOHExists,
    Optional,
    UniqueField,
    UniqueFieldChanged,
    ValidationGroup,
    Validator,
)


class NoVoicemailAssociated(Validator):
    def validate(self, user):
        if user.voicemail:
            raise errors.resource_associated(
                'User', 'Voicemail', user_id=user.id, voicemail_id=user.voicemail.id
            )


class NoEmptyFieldWhenEnabled(Validator):
    def __init__(self, field, enabled):
        self.field = field
        self.enabled = enabled

    def validate(self, model):
        if getattr(model, self.enabled):
            if getattr(model, self.field) is None:
                raise errors.forward_destination_null()


def build_validator():
    moh_validator = MOHExists('music_on_hold', moh_dao.get_by)
    return ValidationGroup(
        delete=[NoVoicemailAssociated()],
        create=[
            Optional(
                'email',
                UniqueField(
                    'email', lambda email: user_dao.find_by(email=email), 'User'
                ),
            ),
            Optional(
                'username',
                UniqueField(
                    'username',
                    lambda username: user_dao.find_by(username=username),
                    'User',
                ),
            ),
            moh_validator,
        ],
        edit=[
            Optional('email', UniqueFieldChanged('email', user_dao.find_by, 'User')),
            Optional(
                'username', UniqueFieldChanged('username', user_dao.find_by, 'User')
            ),
            moh_validator,
        ],
    )


def build_validator_forward():
    return ValidationGroup(
        edit=[
            Optional(
                'busy_enabled',
                NoEmptyFieldWhenEnabled('busy_destination', 'busy_enabled'),
            ),
            Optional(
                'noanswer_enabled',
                NoEmptyFieldWhenEnabled('noanswer_destination', 'noanswer_enabled'),
            ),
            Optional(
                'unconditional_enabled',
                NoEmptyFieldWhenEnabled(
                    'unconditional_destination', 'unconditional_enabled'
                ),
            ),
        ]
    )
