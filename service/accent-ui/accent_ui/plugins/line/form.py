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
from accent_ui.plugins.sip_template.form import EndpointSIPForm


class SCCPOptionsForm(BaseForm):
    option_key = SelectField(choices=[], validators=[InputRequired()])
    option_value = StringField(validators=[InputRequired()])


class EndpointSCCPForm(BaseForm):
    id = HiddenField()
    options = FieldList(FormField(SCCPOptionsForm))


class EndpointCustomForm(BaseForm):
    id = HiddenField()
    interface = StringField(l_('Interface'), validators=[InputRequired()])
    interface_suffix = StringField(l_('Interface Suffix'), validators=[Length(max=32)])


class LineForm(BaseForm):
    context = SelectField(l_('Context'), validators=[InputRequired()], choices=[])
    protocol = SelectField(
        choices=[('sip', l_('SIP')), ('sccp', l_('SCCP')), ('custom', l_('CUSTOM'))]
    )
    endpoint_sip = FormField(EndpointSIPForm)
    endpoint_sccp = FormField(EndpointSCCPForm)
    endpoint_custom = FormField(EndpointCustomForm)
    submit = SubmitField(l_('Submit'))
