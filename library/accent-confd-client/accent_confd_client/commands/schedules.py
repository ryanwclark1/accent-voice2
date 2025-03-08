# Copyright 2023 Accent Communications

from accent_confd_client.crud import MultiTenantCommand


class SchedulesCommand(MultiTenantCommand):
    resource = 'schedules'
