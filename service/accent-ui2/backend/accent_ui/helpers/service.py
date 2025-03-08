from accent_confd_client import Client as ConfdClient
from fastapi import Depends

from accent_ui.core.client import get_accent_confd_client


class BaseConfdService:
    """
    Base service for resource-related operations.
    """
    def __init__(self, confd_client: ConfdClient):
        self._confd = confd_client
        self.resource_confd = None

    def list(self, limit=None, order=None, direction=None, offset=None, search=None, **kwargs):
        """
        Lists resources with optional filtering, ordering, and pagination.

        Args:
            limit (int, optional): The maximum number of resources to return.
            order (str, optional): The field to order the resources by.
            direction (str, optional): The direction to order the resources ('asc' or 'desc').
            offset (int, optional): The number of resources to skip before starting to
            collect the result set.
            search (str, optional): A search term to filter the resources.
            **kwargs: Additional keyword arguments for filtering.

        Returns:
            list: A list of resources.
        """
        resource_client = getattr(self._confd, self.resource_confd)
        return resource_client.list(
            search=search,
            order=order,
            limit=limit,
            direction=direction,
            offset=offset,
            **kwargs,
        )

    def get(self, resource_id):
        """
        Retrieves a resource by its ID.

        Args:
            resource_id (str): The ID of the resource to retrieve.

        Returns:
            dict: The retrieved resource.
        """
        resource_client = getattr(self._confd, self.resource_confd)
        return resource_client.get(resource_id)

    def update(self, resource):
        """
        Updates a resource.

        Args:
            resource (dict): The resource data to update.

        Returns:
            None
        """
        resource_client = getattr(self._confd, self.resource_confd)
        resource_client.update(resource)

    def create(self, resource):
        """
        Creates a new resource.

        Args:
            resource (dict): The resource data to create.

        Returns:
            dict: The created resource.
        """
        resource_client = getattr(self._confd, self.resource_confd)
        return resource_client.create(resource)

    def delete(self, resource_id):
        """
        Deletes a resource by its ID.

        Args:
            resource_id (str): The ID of the resource to delete.

        Returns:
            None
        """
        resource_client = getattr(self._confd, self.resource_confd)
        resource_client.delete(resource_id)

def get_confd_service(confd_client=Depends(get_accent_confd_client)):
    """
    Dependency for injecting BaseConfdService with ConfdClient.
    """
    service = BaseConfdService(confd_client)
    # Optionally set `resource_confd` dynamically if needed
    service.resource_confd = "default_resource_name"  # Replace with your default resource
    return service
