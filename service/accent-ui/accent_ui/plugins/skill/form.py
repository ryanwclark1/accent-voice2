# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_
from wtforms.fields import StringField, SubmitField
from wtforms.validators import InputRequired, Length

from accent_ui.helpers.form import BaseForm


class SkillForm(BaseForm):
    category = StringField(l_('Category'), [InputRequired(), Length(max=64)])
    name = StringField(l_('Name'), [InputRequired(), Length(max=64)])
    description = StringField(l_('Description'), [Length(max=128)])
    submit = SubmitField(l_('Submit'))
