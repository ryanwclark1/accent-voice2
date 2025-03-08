# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_
from wtforms.fields import BooleanField, SelectField, StringField, SubmitField
from wtforms.widgets import PasswordInput

from accent_ui.helpers.form import BaseForm


class HepForm(BaseForm):
    enabled = BooleanField(l_('Enabled'))
    capture_address = StringField(l_('Capture Address'))
    capture_password = StringField(
        l_('Capture Password'), widget=PasswordInput(hide_value=False)
    )
    capture_id = StringField(l_('Capture ID'))
    uuid_type = SelectField(
        l_('UUID Type'),
        choices=[('call-id', l_('Call ID')), ('channel', l_('Channel'))],
    )
    submit = SubmitField(l_('Submit'))
