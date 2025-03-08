# Copyright 2023 Accent Communications

from flask_restful import abort

from accent_confd.database import wizard as wizard_db


def accent_unconfigured(func):
    def wrapper(*args, **kwargs):
        if wizard_db.get_accent_configured().configured:
            abort(403, message='Accent is already configured')
        return func(*args, **kwargs)

    return wrapper
