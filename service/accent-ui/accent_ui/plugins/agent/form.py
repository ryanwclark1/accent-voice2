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


class SkillListForm(BaseForm):
    id = HiddenField()
    skill_id = SelectField(choices=[])
    name = HiddenField()
    skill_weight = StringField()


class AgentForm(BaseForm):
    firstname = StringField(l_('Firstname'), [InputRequired(), Length(max=128)])
    lastname = StringField(l_('Lastname'), [Length(max=128)])
    number = StringField(l_('Agent Number'), [InputRequired(), Length(max=128)])
    description = StringField(l_('Description'), [Length(max=128)])
    preprocess_subroutine = StringField(l_('Subroutine'), [Length(max=79)])
    password = StringField(l_('Password'), [Length(max=128)])
    language = StringField(l_('Language'), [Length(max=128)])
    skills = FieldList(FormField(SkillListForm))
    submit = SubmitField(l_('Submit'))
