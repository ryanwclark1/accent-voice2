# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    FieldList,
    FormField,
    HiddenField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired

from accent_ui.helpers.form import BaseForm


class ExtensionForm(BaseForm):
    exten = StringField(l_('Extension'), validators=[InputRequired()])
    context = SelectField(l_('Context'), validators=[InputRequired()], choices=[])
    submit = SubmitField(l_('Submit'))


class FeaturesForm(BaseForm):
    uuid = HiddenField()
    enabled = BooleanField(l_('Enabled'), default=False)
    feature = StringField(l_('Feature'), validators=[InputRequired()])
    exten = StringField(l_('Extension'), validators=[InputRequired()])


class ExtensionFeaturesForm(BaseForm):
    extensions = FieldList(FormField(FeaturesForm))
    submit = SubmitField(l_('Submit'))


class ExtensionDestinationForm(BaseForm):
    exten = StringField(l_('Extension'), validators=[InputRequired()])
    context = StringField(l_('Context'), validators=[InputRequired()])
