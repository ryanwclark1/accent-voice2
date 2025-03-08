# Copyright 2023 Accent Communications

from sys import maxunicode

MAX_CHAR = chr(maxunicode)
ALMOST_LAST_STRING = MAX_CHAR * 16


class SelfSortingServiceMixin:
    @staticmethod
    def sort(contacts, order=None, direction=None, **_):
        if not order:
            return contacts

        reverse = direction == 'desc'

        def get_value(contact):
            value = contact.get(order)
            return value or ALMOST_LAST_STRING

        return sorted(contacts, key=get_value, reverse=reverse)
