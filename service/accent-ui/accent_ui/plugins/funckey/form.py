# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_
from wtforms.fields import SelectField, StringField
from wtforms.validators import InputRequired, Length

from accent_ui.helpers.form import BaseForm


class CustomFuncKeyDestination(BaseForm):
    exten = StringField(validators=[InputRequired(), Length(max=255)])


class GeneralServicesFuncKeyDestinationForm(BaseForm):
    select_field = 'service'

    service = SelectField(
        l_('Service'),
        choices=[
            ('enablevm', l_('Enable voicemail')),
            ('vmusermsg', l_('Reach the voicemail')),
            ('vmuserpurge', l_('Delete messages from voicemail')),
            ('phonestatus', l_('Phone status')),
            ('recsnd', l_('Sound recording')),
            ('fwdundoall', l_('Disable all forwarding')),
            ('calllistening', l_('Listen to online calls')),
            ('directoryaccess', l_('Directory access')),
            ('pickup', l_('Group Interception')),
            ('callrecord', l_('Call recording')),
            ('incallfilter', l_('Incoming call filtering')),
            ('enablednd', l_('Do not disturb')),
        ],
        validators=[InputRequired()],
    )


class TransferServicesFuncKeyDestinationForm(BaseForm):
    select_field = 'transfer'

    transfer = SelectField(
        l_('Transfer'),
        choices=[
            ('blind', l_('Blind transfer')),
            ('attended', l_('Indirect transfer')),
        ],
        validators=[InputRequired()],
    )


class ForwardServicesFuncKeyDestinationForm(BaseForm):
    select_field = 'forward'

    forward = SelectField(
        l_('Forward'),
        choices=[
            ('busy', l_('Enable / Disable forwarding on busy')),
            ('noanswer', l_('Enable / Disable forwarding on no answer')),
            ('unconditional', l_('Enable / Disable forwarding unconditional')),
        ],
        validators=[InputRequired()],
    )

    exten = StringField(l_('Exten'), validators=[Length(max=255)])


class OnlineRecFuncKeyDestinationForm(BaseForm):
    pass
