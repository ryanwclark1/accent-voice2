# Copyright 2023 Accent Communications

from wtforms.fields import (
    BooleanField,
    FieldList,
    FormField,
    HiddenField,
    SelectField,
    SubmitField,
)
from wtforms.validators import InputRequired

from accent_ui.helpers.form import BaseForm


class ServicesForm(BaseForm):
    uuid = SelectField(choices=[], validators=[InputRequired()])
    favorites = BooleanField()
    reverse = BooleanField()
    lookup = BooleanField()


class DirdProfileForm(BaseForm):
    uuid = HiddenField()
    services = FieldList(FormField(ServicesForm))
    submit = SubmitField()
