# Copyright 2023 Accent Communications

import logging
import time
from functools import wraps

from accent import mallow_helpers, rest_api_helpers
from accent.flask.auth_verifier import AuthVerifierFlask
from flask_restful import Resource

logger = logging.getLogger(__name__)

auth_verifier = AuthVerifierFlask()


def handle_api_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except rest_api_helpers.APIException as error:
            response = {
                'reason': [error.message],
                'timestamp': time.time(),
                'status_code': error.status_code,
            }
            logger.error('%s: %s', error.message, error.details)
            return response, error.status_code

    return wrapper


class LegacyErrorCatchingResource(Resource):
    method_decorators = [handle_api_exception] + Resource.method_decorators


class LegacyAuthResource(LegacyErrorCatchingResource):
    method_decorators = [
        auth_verifier.verify_token
    ] + LegacyErrorCatchingResource.method_decorators


class ErrorCatchingResource(Resource):
    method_decorators = [
        mallow_helpers.handle_validation_exception,
        rest_api_helpers.handle_api_exception,
    ] + Resource.method_decorators


class AuthResource(ErrorCatchingResource):
    method_decorators = [
        auth_verifier.verify_tenant,
        auth_verifier.verify_token,
    ] + ErrorCatchingResource.method_decorators
