# Copyright 2023 Accent Communications

import re

AGENT_NUMBER_REGEX = re.compile(r'^\d+$')


def format_agent_member_name(agent_number):
    return f'Agent/{agent_number}'


def format_agent_skills(agent_id):
    return f'agent-{agent_id}'


def is_valid_agent_number(agent_number):
    return AGENT_NUMBER_REGEX.match(agent_number)
