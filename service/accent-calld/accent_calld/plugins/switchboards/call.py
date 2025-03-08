# Copyright 2023 Accent Communications


class QueuedCall:
    def __init__(self, id_):
        self.id = id_
        self.creation_time = None
        self.caller_id_name = ''
        self.caller_id_number = ''


class HeldCall:
    def __init__(self, id_):
        self.id = id_
        self.caller_id_name = ''
        self.caller_id_number = ''
