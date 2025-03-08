# Copyright 2023 Accent Communications


class UnknownReferenceException(Exception):
    def __init__(self, references):
        super().__init__(f"Missing references: {references}")


class DuplicateReferenceException(Exception):
    def __init__(self, reference):
        super().__init__(f"Duplicate reference: {reference}")
