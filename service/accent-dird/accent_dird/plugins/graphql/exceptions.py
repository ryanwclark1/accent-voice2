# Copyright 2023 Accent Communications

import time

from graphql import GraphQLError


class Unauthorized(GraphQLError):
    def __init__(self):
        super().__init__(message='Unauthorized')


class AuthServerUnreachable(GraphQLError):
    def __init__(self, auth_config):
        message = f'Authentication server {auth_config["host"]}:{auth_config["port"]} unreachable'
        super().__init__(message)


def graphql_error_from_api_exception(e):
    extensions = {
        'error_id': e.id_,
        'details': e.details or {},
        'timestamp': time.time(),
    }
    if e.resource:
        extensions['resource'] = e.resource
    return GraphQLError(e.message, extensions=extensions)
