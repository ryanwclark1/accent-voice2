# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    FileField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired, Length

from accent_ui.helpers.destination import DestinationHiddenField
from accent_ui.helpers.form import BaseForm


class SoundFilenameForm(BaseForm):
    name = FileField(l_('Name'), validators=[InputRequired(), Length(max=255)])
    format = StringField(l_('Format'), validators=[Length(max=10)])
    language = StringField(l_('Language'), validators=[Length(max=10)])
    text = StringField(l_('Text'))
    path = StringField(l_('Path'))
    submit = SubmitField(l_('Submit'))


class SoundForm(BaseForm):
    name = StringField(l_('Name'), validators=[InputRequired(), Length(max=255)])
    submit = SubmitField(l_('Submit'))


class SoundDestinationForm(BaseForm):
    set_value_template = '{name} [{format}] ({language})'

    filename = SelectField(
        l_('Filename'), choices=[], validators=[InputRequired(), Length(max=255)]
    )
    name = DestinationHiddenField()
    language = DestinationHiddenField()
    format = DestinationHiddenField()
    skip = BooleanField(l_('Skip'), default=False)
    no_answer = BooleanField(l_('No Answer'), default=False)
