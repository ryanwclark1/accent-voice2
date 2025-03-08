# Copyright 2023 Accent Communications


class Hint:
    __slots__ = ['user_id', 'conference_id', 'extension', 'argument']

    def __init__(self, user_id=None, conference_id=None, extension=None, argument=None):
        self.user_id = user_id
        self.conference_id = conference_id
        self.extension = extension
        self.argument = argument

    def __eq__(self, other):
        return (
            self.user_id == other.user_id
            and self.conference_id == other.conference_id
            and self.extension == other.extension
            and self.argument == other.argument
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return f'Hint(user_id={self.user_id}, conference_id={self.conference_id}, extension={self.extension}, argument={self.argument})'
