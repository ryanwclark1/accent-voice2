# Copyright 2023 Accent Communications

import logging

from .exceptions import InvalidEvent

logger = logging.getLogger(__name__)


class TransferRecipientAnsweredEvent:
    def __init__(self, event):
        try:
            self.transfer_bridge = event['args'][2]
        except (KeyError, IndexError):
            raise InvalidEvent(event)


class CreateTransferEvent:
    def __init__(self, event):
        try:
            self.transfer_id = event['args'][2]
        except (KeyError, IndexError):
            raise InvalidEvent(event)
