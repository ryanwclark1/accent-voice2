# Copyright 2023 Accent Communications

from accent.flask.headers import extract_token_id_from_query_or_header
from flask import Response

from accent_auth import http


class EmailConfirm(http.AuthResource):
    def __init__(self, email_service, template_formatter, config):
        self.email_service = email_service
        self._mimetype = config['email_confirmation_get_mimetype']
        self._get_body = template_formatter.get_confirmation_email_get_body()

    @http.required_acl(
        'auth.emails.{email_uuid}.confirm.edit',
        extract_token_id=extract_token_id_from_query_or_header,
    )
    def get(self, email_uuid):
        self.email_service.confirm(email_uuid)
        return Response(self._get_body, 200, mimetype=self._mimetype)

    @http.required_acl('auth.emails.{email_uuid}.confirm.edit')
    def put(self, email_uuid):
        self.email_service.confirm(email_uuid)
        return '', 204
