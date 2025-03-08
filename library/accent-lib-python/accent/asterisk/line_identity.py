# Copyright 2023 Accent Communications

from __future__ import annotations


def identity_from_channel(channel: str) -> str:
    last_dash = channel.rfind('-')
    if channel.startswith('Local/'):
        end = channel[-2:]
    else:
        end = ''
    return channel[:last_dash].lower() + end
