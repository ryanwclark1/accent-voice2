# Copyright 2023 Accent Communications

from __future__ import annotations


def action(type_: str | None, subtype: str | None = None) -> str:
    type_ = type_ or ''
    subtype = f':{subtype}' if subtype else ''
    return f'{type_}{subtype}'


def action_type(action: str | None) -> str | None:
    return action.split(':', 1)[0] if action else None


def action_subtype(action: str | None) -> str | None:
    type_subtype = action.split(':', 1) if action else ''
    return type_subtype[1] if len(type_subtype) == 2 else None
