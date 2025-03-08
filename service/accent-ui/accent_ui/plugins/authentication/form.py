# Copyright 2023 Accent Communications

import logging

import requests
from accent_auth_client import Client as AuthClient
from flask import session
from flask_babel import lazy_gettext as l_
from flask_wtf import FlaskForm
from requests.exceptions import HTTPError
from wtforms.fields import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, ValidationError

from accent_ui.http_server import app
from accent_ui.user import UserUI

USERNAME_PASSWORD_ERROR = l_('Wrong username and/or password')
TOO_MANY_SESSIONS_ERROR = l_('Too many active sessions')

logger = logging.getLogger(__name__)


def unauthorized(error):
    return error.response is not None and error.response.status_code == 401


def limit_reached(error):
    return error.response is not None and error.response.status_code == 429


class LoginForm(FlaskForm):
    username = StringField(l_('Username'), validators=[InputRequired()])
    password = PasswordField(l_('Password'), validators=[InputRequired()])
    language = SelectField(l_('Language'))
    submit = SubmitField(
        l_('Login'),
        render_kw={
            'data-loading-text': "<i class='fa fa-circle-o-notch fa-spin'></i> Processing..."
        },
    )

    def validate(self):
        super().validate()
        try:
            auth_client = AuthClient(
                username=self.username.data,
                password=self.password.data,
                **app.config['auth'],
            )
            response = auth_client.token.new(expiration=60 * 60 * 12)
            auth_client.set_token(response['token'])
            user = auth_client.users.get(response['metadata']['uuid'])
            user['password'] = self.password.data
            session['user'] = user
        except HTTPError as e:
            if unauthorized(e):
                self.username.errors.append(USERNAME_PASSWORD_ERROR)
                self.password.errors.append(USERNAME_PASSWORD_ERROR)
                return False
            message = TOO_MANY_SESSIONS_ERROR if limit_reached(e) else e.message
            raise ValidationError(
                l_('Error with Accent authentication server: %(error)s', error=message)
            )
        except requests.ConnectionError:
            raise ValidationError(l_('Accent authentication server connection error'))

        self.user = UserUI(response['token'], response['auth_id'])
        self.user.set_config(app.config)

        return True
