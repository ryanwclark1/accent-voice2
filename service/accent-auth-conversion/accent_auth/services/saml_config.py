# Copyright 2023 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any
from xml.etree import ElementTree

from accent_auth.database.models import Domain, SAMLConfig

if TYPE_CHECKING:
    from accent_auth.database.queries import DAO

from accent_auth.exceptions import (
    DuplicatedSAMLConfigException,
    SAMLConfigParameterException,
)
from accent_auth.plugins.http.saml_config.schemas import SamlConfigWithMetadata
from accent_auth.services.helpers import BaseService
from accent_auth.services.saml import Config, SAMLService

logger = logging.getLogger(__name__)


class SAMLConfigService(BaseService):
    def __init__(self, config: Config, saml_service: SAMLService, dao: DAO) -> None:
        super().__init__(dao)
        self._acs_url_template = config['saml']['acs_url_template']
        self._saml_service = saml_service
        self._reload_saml_service()

    def get(self, tenant_uuid: str) -> dict[str, str]:
        return self._dao.saml_config.get(tenant_uuid)

    def create(
        self, tenant_uuid: str, saml_config, etree_metadata: ElementTree.ElementTree
    ) -> dict[str, Any]:
        metadata = ElementTree.tostring(etree_metadata.getroot()).decode()
        kwargs = {
            'tenant_uuid': tenant_uuid,
            'domain_uuid': saml_config['domain_uuid'],
            'entity_id': saml_config['entity_id'],
            'idp_metadata': metadata,
            'acs_url': saml_config['acs_url'],
        }
        if self._dao.saml_config.exists(tenant_uuid):
            raise DuplicatedSAMLConfigException(tenant_uuid)
        elif saml_config['domain_uuid'] not in [
            i.uuid for i in self._dao.domain.list(tenant_uuid=tenant_uuid)
        ]:
            raise SAMLConfigParameterException(
                tenant_uuid, 'Domain not from tenant', 400
            )
        else:
            result: dict[str, Any] = self._dao.saml_config.create(**kwargs)
        self._reload_saml_service()
        return result

    def update(self, tenant_uuid: str, kwargs, etree_metadata) -> dict[str, Any]:
        kwargs['tenant_uuid'] = tenant_uuid

        if domain_uuid := kwargs.get('domain_uuid'):
            if domain_uuid not in [
                i.uuid for i in self._dao.domain.list(tenant_uuid=tenant_uuid)
            ]:
                raise SAMLConfigParameterException(
                    tenant_uuid, 'Domain not from tenant', 400
                )

        if etree_metadata:
            kwargs['idp_metadata'] = ElementTree.tostring(
                etree_metadata.getroot()
            ).decode()

        result: dict[str, Any] = self._dao.saml_config.update(**kwargs)
        self._reload_saml_service()
        return result

    def delete(self, tenant_uuid: str) -> None:
        self._dao.saml_config.delete(tenant_uuid)
        self._reload_saml_service()

    def get_metadata(self, tenant_uuid: str) -> ElementTree.Element:
        etree_metadata: ElementTree.Element = ElementTree.fromstring(
            self._dao.saml_config.get(tenant_uuid)['idp_metadata']
        )
        return etree_metadata

    def get_acs_url_template(self) -> dict[str, str]:
        return {'acs_url': self._acs_url_template}

    def _update_domain_name(self, item, domains) -> dict[str, str]:
        domain_name: list[str] = [
            domain.name for domain in domains if domain.uuid == item['domain_uuid']
        ]
        if domain_name:
            item['domain_name'] = domain_name[0]
            return item
        logger.error(
            'Database consistency error, missing domain name for %s/%s', item, domains
        )
        logger.info('SAML configuration for domain_uuid: %s couldn\'t be loaded', item)
        raise SAMLConfigParameterException(
            f'unknown tenant, domain_uuid: {item}',
            f'Database consistency error, missing domain name for domain_uuid {item}',
            500,
        )

    def _update_item(self, item, domains) -> dict[str, str]:
        updated: dict[str, str] = self._update_domain_name(item, domains)
        return updated

    def _reload_saml_service(self) -> None:
        db_configs: list[SAMLConfig] = self._dao.saml_config.list()
        domains: list[Domain] = self._dao.domain.list()
        saml_configs = [SamlConfigWithMetadata().dump(item) for item in db_configs]
        configs_with_domain_names: list[dict[str, str]] = [
            self._update_item(item, domains) for item in saml_configs
        ]
        self._saml_service.init_clients(configs_with_domain_names)
        return None
