# Copyright 2023 Accent Communications


def escape(routing_key_part: str) -> str:
    return (
        routing_key_part.replace('.', '__DOT__')
        .replace('#', '__HASH__')
        .replace('*', '__STAR__')
    )
