# Copyright 2023 Accent Communications

import sys
from operator import attrgetter

import accent_agentd_client
import accent_auth_client
from accent.cli import BaseCommand, Interpreter, UsageError
from accent.token_renewer import TokenRenewer

from accent_agentd_cli.config import load as load_config


def main():
    config = load_config(sys.argv[1:])

    token_renewer = TokenRenewer(_new_auth_client(config), expiration=600)
    agent_client = _new_agent_client(config)

    interpreter = Interpreter(
        prompt='accent-agentd-cli> ', history_file='~/.accent_agentd_cli_history'
    )
    interpreter.add_command('add', AddAgentToQueueCommand(agent_client))
    interpreter.add_command('remove', RemoveAgentFromQueueCommand(agent_client))
    interpreter.add_command('login', LoginCommand(agent_client))
    interpreter.add_command('logoff', LogoffCommand(agent_client))
    interpreter.add_command('relog all', RelogAllCommand(agent_client))
    interpreter.add_command('pause', PauseCommand(agent_client))
    interpreter.add_command('unpause', UnpauseCommand(agent_client))
    interpreter.add_command('status', StatusCommand(agent_client))

    token_renewer.subscribe_to_token_change(agent_client.set_token)
    with token_renewer:
        if config.get('command'):
            interpreter.execute_command_line(config['command'])
        else:
            interpreter.loop()


def _new_agent_client(config):
    return accent_agentd_client.Client(**config['agentd'])


def _new_auth_client(config):
    auth_config = dict(config['auth'])
    username = auth_config.pop('service_id')
    password = auth_config.pop('service_key')
    del auth_config['key_file']
    return accent_auth_client.Client(username=username, password=password, **auth_config)


class BaseAgentClientCommand(BaseCommand):
    def __init__(self, agent_client):
        BaseCommand.__init__(self)
        self._agent_client = agent_client

    def execute(self):
        raise NotImplementedError()


class AddAgentToQueueCommand(BaseAgentClientCommand):

    help = 'Add agent to queue'
    usage = '<agent_id> <queue_id>'

    def prepare(self, command_args):
        try:
            agent_id = int(command_args[0])
            queue_id = int(command_args[1])
            return (agent_id, queue_id)
        except Exception:
            raise UsageError()

    def execute(self, agent_id, queue_id):
        self._agent_client.agents.add_agent_to_queue(agent_id, queue_id)


class RemoveAgentFromQueueCommand(BaseAgentClientCommand):

    help = 'Remove agent from queue'
    usage = '<agent_id> <queue_id>'

    def prepare(self, command_args):
        try:
            agent_id = int(command_args[0])
            queue_id = int(command_args[1])
            return (agent_id, queue_id)
        except Exception:
            raise UsageError()

    def execute(self, agent_id, queue_id):
        self._agent_client.agents.remove_agent_from_queue(agent_id, queue_id)


class LoginCommand(BaseAgentClientCommand):

    help = 'Login agent'
    usage = '<agent_number> <extension> <context>'

    def prepare(self, command_args):
        try:
            agent_number = command_args[0]
            extension = command_args[1]
            context = command_args[2]
            return (agent_number, extension, context)
        except Exception:
            raise UsageError()

    def execute(self, agent_number, extension, context):
        self._agent_client.agents.login_agent_by_number(
            agent_number, extension, context
        )


class LogoffCommand(BaseAgentClientCommand):

    help = 'Logoff agent'
    usage = '(<agent_number> | all)'

    def prepare(self, command_args):
        try:
            agent_number = command_args[0]
            return (agent_number,)
        except Exception:
            raise UsageError()

    def execute(self, agent_number):
        if agent_number == 'all':
            self._execute_all()
        else:
            self._execute(agent_number)

    def _execute_all(self):
        self._agent_client.agents.logoff_all_agents()

    def _execute(self, agent_number):
        self._agent_client.agents.logoff_agent_by_number(agent_number)


class RelogAllCommand(BaseAgentClientCommand):

    help = 'Relog all currently logged agents'
    usage = '[--timeout <timeout>]'

    def prepare(self, command_args):
        try:
            timeout_flag = len(command_args) > 0 and command_args[0] == '--timeout'
            timeout = int(command_args[1]) if timeout_flag else None
            return (timeout,)
        except Exception:
            raise UsageError()

    def execute(self, timeout):
        self._agent_client.agents.relog_all_agents(recurse=True, timeout=timeout)


class PauseCommand(BaseAgentClientCommand):

    help = 'Pause agent'
    usage = '<agent_number>'

    def prepare(self, command_args):
        try:
            agent_number = command_args[0]
            return (agent_number,)
        except Exception:
            raise UsageError()

    def execute(self, agent_number):
        self._agent_client.agents.pause_agent_by_number(agent_number)


class UnpauseCommand(BaseAgentClientCommand):

    help = 'Unpause agent'
    usage = '<agent_number>'

    def prepare(self, command_args):
        try:
            agent_number = command_args[0]
            return (agent_number,)
        except Exception:
            raise UsageError()

    def execute(self, agent_number):
        self._agent_client.agents.unpause_agent_by_number(agent_number)


class StatusCommand(BaseAgentClientCommand):

    help = 'Get status of agent'
    usage = '[<agent_number>]'

    def prepare(self, command_args):
        if command_args:
            agent_number = command_args[0]
        else:
            agent_number = None
        return (agent_number,)

    def execute(self, agent_number):
        if agent_number is None:
            self._execute_all()
        else:
            self._execute(agent_number)

    def _execute_all(self):
        agent_statuses = self._agent_client.agents.get_agent_statuses(recurse=True)
        for agent_status in sorted(agent_statuses, key=attrgetter('number')):
            _print_agent_status(agent_status)

    def _execute(self, agent_number):
        agent_status = self._agent_client.agents.get_agent_status_by_number(
            agent_number
        )
        _print_agent_status(agent_status)


def _print_agent_status(agent_status):
    print(f'Agent/{agent_status.number} (ID {agent_status.id})')
    print(f'    logged: {agent_status.logged}')
    if agent_status.logged:
        print(f'    extension: {agent_status.extension}')
        print(f'    context: {agent_status.context}')
        print(f'    state interface: {agent_status.state_interface}')


if __name__ == '__main__':
    main()
