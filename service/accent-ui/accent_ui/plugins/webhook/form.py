# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    HiddenField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import InputRequired, Length

from accent_ui.helpers.form import BaseForm


class WebhookForm(BaseForm):
    name = StringField(l_('Display name'), [Length(max=100)])
    events = SelectMultipleField(
        l_('Event Name'), [InputRequired(), Length(max=128)], choices=[]
    )
    services = SelectField(l_('Services'), choices=[])
    events_user_uuid = HiddenField()
    user_uuid = SelectField(l_('User'), choices=[])


class WebhookFormHTTP(WebhookForm):
    url = StringField(l_('Target'), [InputRequired(), Length(max=512)])
    method = SelectField(
        l_('Method'),
        choices=[
            ('post', l_('POST')),
            ('get', l_('GET')),
            ('put', l_('PUT')),
            ('delete', l_('DELETE')),
            ('head', l_('HEAD')),
        ],
    )
    content_type = StringField(
        l_('Content Type'), [Length(max=100)], default='application/json'
    )
    verify_certificate = BooleanField(l_('Verify Certificate'), default=False)
    body = TextAreaField(l_('Body'))
    submit = SubmitField(l_('Submit'))
