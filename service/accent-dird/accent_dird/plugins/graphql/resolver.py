# Copyright 2023 Accent Communications
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flask import request

from accent_dird import auth
from accent_dird.exception import NoSuchProfile, NoSuchProfileAPIException

from . import schema
from .exceptions import graphql_error_from_api_exception

if TYPE_CHECKING:
    from typing import TypedDict

    from graphql import GraphQLResolveInfo

    from accent_dird.plugins.source_result import _SourceResult

    class ContextDict(TypedDict):
        resolver: Resolver
        token_id: str
        user_uuid: str
        tenant_uuid: str

    class ResolveInfo(GraphQLResolveInfo):
        context: ContextDict


class Resolver:
    def __init__(self, profile_service, reverse_service):
        self.profile_service = profile_service
        self.reverse_service = reverse_service

    def hello(self, root: _SourceResult, info: GraphQLResolveInfo, **args: Any) -> str:
        return 'world'

    def get_user_me(
        self, root: _SourceResult, info: ResolveInfo, **args: Any
    ) -> dict[str, Any]:
        token = request.headers['X-Auth-Token']
        token_info = auth.client().token.get(token)
        metadata = token_info['metadata']
        info.context['token_id'] = token
        info.context['user_uuid'] = metadata['uuid']
        info.context['tenant_uuid'] = metadata['tenant_uuid']
        return {}

    def get_user_me_uuid(
        self, root: _SourceResult, info: ResolveInfo, **args: Any
    ) -> str:
        return info.context['user_uuid']

    def get_user_contacts(
        self, root: _SourceResult, info: ResolveInfo, **args: Any
    ) -> list[Any]:
        user_uuid = info.context['user_uuid']
        tenant_uuid = info.context['tenant_uuid']
        token_id = info.context['token_id']
        profile = args['profile']
        try:
            profile_config = self.profile_service.get_by_name(tenant_uuid, profile)
        except NoSuchProfile as e:
            raise graphql_error_from_api_exception(NoSuchProfileAPIException(e.profile))

        if args.get('extens'):
            return self.reverse_service.reverse_many(
                profile_config,
                args['extens'],
                profile,
                user_uuid=user_uuid,
                token=token_id,
            )
        return []

    def get_contact_type(
        self, contact: _SourceResult, info: ResolveInfo
    ) -> type[schema.AccentContact] | type[schema.Contact]:
        if contact.backend == 'accent':
            return schema.AccentContact
        return schema.Contact

    def get_contact_field(self, contact: _SourceResult, info: ResolveInfo, **args: Any):
        return contact.fields.get(info.field_name)

    def get_contact_related_field(
        self, contact: _SourceResult, info: ResolveInfo, **args: Any
    ):
        return contact.relations.get(info.field_name.replace('Id', '_id'))

    def get_contact_user_uuid(
        self, contact: _SourceResult, info: ResolveInfo, **args: Any
    ):
        return contact.relations['user_uuid']

    def get_reverse_field(self, contact: _SourceResult, info: ResolveInfo, **args: Any):
        return contact.fields['reverse']

    def get_source_entry_id(
        self, contact: _SourceResult, info: ResolveInfo, **args: Any
    ):
        return None if contact.source_entry_id is None else contact.source_entry_id()

    def get_source_name(self, contact: _SourceResult, info: ResolveInfo, **args: Any):
        return contact.source

    def get_backend(self, contact: _SourceResult, info: ResolveInfo, **args: Any):
        return contact.backend
