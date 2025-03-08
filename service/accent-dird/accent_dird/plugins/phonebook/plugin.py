# Copyright 2023 Accent Communications
from __future__ import annotations

from typing import TypedDict

from flask_restful import Api

from accent_dird import BaseViewPlugin
from accent_dird.plugin_manager import ViewDependencies
from accent_dird.plugins.phonebook_service.plugin import _PhonebookService

from .http import (
    PhonebookAll,
    PhonebookContactAll,
    PhonebookContactImport,
    PhonebookContactOne,
    PhonebookOne,
)


class Services(TypedDict):
    phonebook: _PhonebookService


class Dependencies(ViewDependencies):
    api: Api
    services: Services


class PhonebookViewPlugin(BaseViewPlugin):
    def load(self, dependencies: Dependencies):
        api = dependencies['api']
        args = (dependencies['services'].get('phonebook'),)

        api.add_resource(
            PhonebookContactAll,
            '/phonebooks/<uuid:phonebook_uuid>/contacts',
            resource_class_args=args,
        )
        api.add_resource(
            PhonebookContactImport,
            '/phonebooks/<uuid:phonebook_uuid>/contacts/import',
            resource_class_args=args,
        )
        api.add_resource(
            PhonebookContactOne,
            '/phonebooks/<uuid:phonebook_uuid>/contacts/<contact_uuid>',
            resource_class_args=args,
        )
        api.add_resource(
            PhonebookAll,
            '/phonebooks',
            resource_class_args=args,
        )
        api.add_resource(
            PhonebookOne,
            '/phonebooks/<uuid:phonebook_uuid>',
            resource_class_args=args,
        )
