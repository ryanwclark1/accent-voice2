# Copyright 2023 Accent Communications

from accent import mallow_helpers, rest_api_helpers
from accent.auth_verifier import AuthVerifier
from flask_restful import Resource

auth_verifier = AuthVerifier()


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
