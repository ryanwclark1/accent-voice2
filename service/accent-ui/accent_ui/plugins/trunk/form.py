# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    FieldList,
    FormField,
    HiddenField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired, Length
from wtforms.widgets import PasswordInput

from accent_ui.helpers.form import BaseForm
from accent_ui.plugins.sip_template.form import EndpointSIPForm


class EndpointCustomForm(BaseForm):
    id = HiddenField()
    interface = StringField(l_('Interface'), validators=[InputRequired()])
    interface_suffix = StringField(l_('Interface Suffix'), validators=[Length(max=32)])


class OptionsForm(BaseForm):
    option_key = StringField(validators=[InputRequired()])
    option_value = StringField(validators=[InputRequired()])


class EndpointIaxForm(BaseForm):
    id = HiddenField()
    name = StringField(l_('Name'), validators=[InputRequired(), Length(max=40)])
    type = SelectField(
        l_('Type'),
        choices=[('user', l_('User')), ('peer', l_('Peer')), ('friend', l_('Friend'))],
    )
    host = SelectField(
        l_('Host'),
        validators=[InputRequired(), Length(max=255)],
        choices=[('dynamic', l_('Dynamic')), ('static', l_('Static'))],
    )
    host_value = StringField('', validators=[Length(max=255)])
    options = FieldList(FormField(OptionsForm))


class RegisterIAXForm(BaseForm):
    id = HiddenField()
    enabled = BooleanField(l_('Enabled'), default=False)
    auth_username = StringField(l_('Authentication Username'))
    auth_password = StringField(
        l_('Authentication Password'), widget=PasswordInput(hide_value=False)
    )
    callback_context = StringField(l_('Callback Context'))
    callback_extension = StringField(l_('Callback Extension'))
    remote_host = StringField(l_('Remote Host'), validators=[InputRequired()])
    remote_port = IntegerField(l_('Remote port'))


class TrunkForm(BaseForm):
    context = SelectField(l_('Context'), choices=[])
    protocol = SelectField(
        choices=[('sip', l_('SIP')), ('iax', l_('IAX')), ('custom', l_('CUSTOM'))]
    )
    outgoing_caller_id_format = SelectField(
        choices=[
            ('+E164', l_('+E164')),
            ('E164', l_('E164')),
            ('national', l_('National')),
        ]
    )
    endpoint_sip = FormField(EndpointSIPForm)
    endpoint_iax = FormField(EndpointIaxForm)
    endpoint_custom = FormField(EndpointCustomForm)
    register_iax = FormField(RegisterIAXForm)
    submit = SubmitField(l_('Submit'))
