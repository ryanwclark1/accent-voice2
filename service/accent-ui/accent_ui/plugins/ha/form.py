# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_
from wtforms.fields import SelectField, StringField, SubmitField
from wtforms.validators import InputRequired

from accent_ui.helpers.form import BaseForm


class HaForm(BaseForm):
    node_type = SelectField(
        l_('Node Type'),
        choices=[
            ('disabled', l_('Disabled')),
            ('master', l_('Master')),
            ('slave', l_('Slave')),
        ],
        validators=[InputRequired()],
    )
    remote_address = StringField(l_('Remote address'), validators=[InputRequired()])
    submit = SubmitField(l_('Submit'))
