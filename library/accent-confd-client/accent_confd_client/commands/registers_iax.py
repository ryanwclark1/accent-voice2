# Copyright 2023 Accent Communications

from accent_confd_client.crud import CRUDCommand


class RegistersIAXCommand(CRUDCommand):
    resource = 'registers/iax'
