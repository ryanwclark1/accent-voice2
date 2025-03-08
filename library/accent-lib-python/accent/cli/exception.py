# Copyright 2023 Accent Communications


class CommandAlreadyRegisteredError(Exception):
    pass


class NoMatchingCommandError(Exception):
    pass


class UsageError(Exception):
    pass
