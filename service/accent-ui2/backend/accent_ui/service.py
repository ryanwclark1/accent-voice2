from fastapi import Depends
from helpers.service import BaseConfdExtensionService

from accent_ui.core.client import get_accent_confd_client


def get_extension_service(confd_client=Depends(get_accent_confd_client)):
    """
    Dependency for injecting the BaseConfdExtensionService into FastAPI endpoints.
    """
    service = BaseConfdExtensionService(confd_client)
    # Optionally set `resource_confd` dynamically based on your use case
    service.resource_confd = "default_resource_name"
    return service
