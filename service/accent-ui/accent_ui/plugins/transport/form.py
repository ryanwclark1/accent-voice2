# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FieldList,
    FormField,
    HiddenField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired, Length

from accent_ui.helpers.form import BaseForm


class TransportOptionsForm(BaseForm):
    def to_dict(self):
        return super().to_dict(empty_string=True)

    id = HiddenField()
    option_key = SelectField(
        choices=[],
        validators=[InputRequired()],
    )
    option_value = StringField()


class TransportForm(BaseForm):
    name = StringField(l_('Name'), [InputRequired(), Length(max=128)])
    options = FieldList(FormField(TransportOptionsForm))
    submit = SubmitField(l_('Submit'))
