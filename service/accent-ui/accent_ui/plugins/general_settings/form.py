# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_
from wtforms.fields import FieldList, FormField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, IPAddress

from accent_ui.helpers.form import BaseForm


class BasePJSIPOptionsForm(BaseForm):
    def to_dict(self):
        return super().to_dict(empty_string=True)

    option_key = SelectField(
        choices=[],
        validators=[InputRequired()],
    )
    option_value = StringField()


class PJSIPGlobalOptionsForm(BasePJSIPOptionsForm):
    pass


class PJSIPSystemOptionsForm(BasePJSIPOptionsForm):
    pass


class OptionsForm(BaseForm):
    def to_dict(self):
        return super().to_dict(empty_string=True)

    option_key = StringField(validators=[InputRequired()])
    option_value = StringField()


class OrderedOptionsForm(BaseForm):
    def to_dict(self):
        return super().to_dict(empty_string=True)

    option_key = StringField(validators=[InputRequired()])
    option_value = StringField()


class GeneralSettingsOptionsForm(BaseForm):
    options = FieldList(FormField(OptionsForm))
    ordered_options = FieldList(FormField(OptionsForm))


class PJSIPGlobalSettingsForm(BaseForm):
    options = FieldList(FormField(PJSIPGlobalOptionsForm))
    submit = SubmitField(l_('Submit'))


class PJSIPSystemSettingsForm(BaseForm):
    options = FieldList(FormField(PJSIPSystemOptionsForm))
    submit = SubmitField(l_('Submit'))


class IaxCallnumberlimitsForm(BaseForm):
    ip_address = StringField(l_('IP Address'), validators=[IPAddress()])
    netmask = StringField(l_('Netmask'))
    limit = StringField(l_('Limit'))


class IaxGeneralSettingsForm(BaseForm):
    general = FormField(GeneralSettingsOptionsForm)
    callnumberlimits = FieldList(FormField(IaxCallnumberlimitsForm))
    submit = SubmitField(l_('Submit'))


class SCCPGeneralSettingsForm(GeneralSettingsOptionsForm):
    submit = SubmitField(l_('Submit'))


class VoicemailZonemessages(BaseForm):
    name = StringField(l_('Name'))
    timezone = SelectField(
        l_('Timezone'),
        validators=[InputRequired()],
        choices=[],
    )
    message = StringField(l_('Message'))


class VoicemailGeneralSettingsForm(BaseForm):
    general = FormField(GeneralSettingsOptionsForm)
    zonemessages = FieldList(FormField(VoicemailZonemessages))
    submit = SubmitField(l_('Submit'))


class FeaturesGeneralSettingsForm(BaseForm):
    general = FormField(GeneralSettingsOptionsForm)
    featuremap = FormField(GeneralSettingsOptionsForm)
    applicationmap = FormField(GeneralSettingsOptionsForm)
    submit = SubmitField(l_('Submit'))


class ConfBridgeGeneralSettingsForm(BaseForm):
    accent_default_bridge = FormField(GeneralSettingsOptionsForm)
    accent_default_user = FormField(GeneralSettingsOptionsForm)
    submit = SubmitField(l_('Submit'))
