# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_

from accent_ui.helpers.funckey import register_funckey_destination_form

from .form import (
    CustomFuncKeyDestination,
    ForwardServicesFuncKeyDestinationForm,
    GeneralServicesFuncKeyDestinationForm,
    OnlineRecFuncKeyDestinationForm,
    TransferServicesFuncKeyDestinationForm,
)


class Plugin:
    def load(self, dependencies):
        register_funckey_destination_form(
            'custom', l_('Custom'), CustomFuncKeyDestination
        )
        register_funckey_destination_form(
            'transfer', l_('Transfer'), TransferServicesFuncKeyDestinationForm
        )
        register_funckey_destination_form(
            'service', l_('Service'), GeneralServicesFuncKeyDestinationForm
        )
        register_funckey_destination_form(
            'forward', l_('Forward'), ForwardServicesFuncKeyDestinationForm
        )
        register_funckey_destination_form(
            'onlinerec', l_('Online Recording'), OnlineRecFuncKeyDestinationForm
        )
