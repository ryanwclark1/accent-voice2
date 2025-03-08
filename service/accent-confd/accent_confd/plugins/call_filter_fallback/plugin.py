# Copyright 2023 Accent Communications

from accent_dao.resources.call_filter import dao as call_filter_dao

from .resource import CallFilterFallbackList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            CallFilterFallbackList,
            '/callfilters/<int:call_filter_id>/fallbacks',
            resource_class_args=(service, call_filter_dao),
        )
