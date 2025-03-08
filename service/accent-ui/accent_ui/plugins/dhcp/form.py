# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_
from wtforms.fields import BooleanField, StringField, SubmitField
from wtforms.validators import InputRequired

from accent_ui.helpers.form import BaseForm


class DhcpForm(BaseForm):
    active = BooleanField(l_('Enabled'), default=False)
    network_interfaces = StringField(l_('Network interface'))
    pool_start = StringField(l_('Pool start'), validators=[InputRequired()])
    pool_end = StringField(l_('Pool end'), validators=[InputRequired()])
    submit = SubmitField(l_('Submit'))
