# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_
from wtforms.fields import FieldList, FormField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length

from accent_ui.helpers.form import BaseForm


class RulesDefinitionForm(BaseForm):
    definition = TextAreaField(l_('Rule'), [InputRequired()])


class SkillRuleForm(BaseForm):
    name = StringField(l_('Name'), [InputRequired(), Length(max=64)])
    rules = FieldList(FormField(RulesDefinitionForm))
    submit = SubmitField(l_('Submit'))
