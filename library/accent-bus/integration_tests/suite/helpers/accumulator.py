# Copyright 2023 Accent Communications

from collections import defaultdict


class MessageAccumulator:
    def __init__(self) -> None:
        self._buffer = defaultdict(list)

    def create_handler(self, event):
        def handler(payload) -> None:
            self.add(event, payload)

        return handler

    def add(self, event, message) -> None:
        event = event if event else "__none__"
        self._buffer[event].append(message)

    def pop(self, event):
        event = event if event else "__none__"
        return self._buffer.pop(event, [])

    def count(self, event):
        return len(self._buffer[event])
