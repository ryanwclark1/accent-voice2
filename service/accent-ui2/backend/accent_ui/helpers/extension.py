import logging

from fastapi import Depends

from accent_ui.core.client import get_accent_confd_client
from accent_ui.helpers.service import BaseConfdService

logger = logging.getLogger(__name__)

class BaseConfdExtensionService(BaseConfdService):
    """
    An extended service class to handle operations related to extensions
    in conjunction with ConfdClient.
    """

    def _extract_main_extension(self, resource):
        """
        Extracts the main extension from the resource.

        Args:
            resource (dict): The resource containing extensions.

        Returns:
            dict: The main extension if it exists, otherwise None.
        """
        extensions = resource.get('extensions')
        if extensions:
            return extensions[0]
        logger.debug('Missing extension resource')

    def create(self, resource):
        """
        Creates a resource and its main extension.

        Args:
            resource (dict): The resource to be created.

        Returns:
            dict: The created resource.
        """
        resource_created = super().create(resource)
        extension = self._extract_main_extension(resource)
        if extension:
            self.create_extension(extension, resource_created)
        return resource_created

    def update(self, resource):
        """
        Updates a resource and its main extension.

        Args:
            resource (dict): The resource to be updated.
        """
        super().update(resource)
        extension = self._extract_main_extension(resource)
        if extension:
            self.update_extension(extension, resource)

    def delete(self, resource_id):
        """
        Deletes a resource and its main extension.

        Args:
            resource_id (str): The ID of the resource to be deleted.
        """
        self.delete_extension(resource_id)
        super().delete(resource_id)

    def create_extension(self, extension, resource):
        """
        Creates an extension for a resource.

        Args:
            extension (dict): The extension to be created.
            resource (dict): The resource to which the extension belongs.
        """
        if resource and extension and extension.get('exten') and extension.get('context'):
            self._add_extension(extension, resource)

    def update_extension(self, extension, resource):
        """
        Updates an extension for a resource.

        Args:
            extension (dict): The extension to be updated.
            resource (dict): The resource to which the extension belongs.
        """
        if not extension or not resource:
            return

        existing_extension = self._get_main_extension(resource)

        if extension.get('exten') and existing_extension:
            self._update_extension(extension, existing_extension)

        elif extension.get('exten'):
            self._add_extension(extension, resource)

        elif not extension.get('exten') and existing_extension:
            self._remove_extension(existing_extension, resource)

    def delete_extension(self, resource_id):
        """
        Deletes extensions for a resource.

        Args:
            resource_id (str): The ID of the resource whose extensions are to be deleted.
        """
        resource_client = getattr(self._confd, self.resource_confd)
        resource = resource_client.get(resource_id)
        for extension in resource.get('extensions', []):
            self._remove_extension(extension, resource)

    def _add_extension(self, extension, resource):
        """
        Adds an extension to a resource.

        Args:
            extension (dict): The extension to be added.
            resource (dict): The resource to which the extension belongs.
        """
        extension = self._confd.extensions.create(extension)
        if extension:
            resource_client = getattr(self._confd, self.resource_confd)
            resource_client(resource).add_extension(extension)

    def _update_extension(self, extension, existing_extension):
        """
        Updates an existing extension.

        Args:
            extension (dict): The new extension data.
            existing_extension (dict): The existing extension data.
        """
        if existing_extension.get('exten') == extension.get('exten') and \
           existing_extension.get('context') == extension.get('context'):
            return
        extension['id'] = existing_extension['id']
        self._confd.extensions.update(extension)

    def _remove_extension(self, extension, resource):
        """
        Removes an extension from a resource.

        Args:
            extension (dict): The extension to be removed.
            resource (dict): The resource from which the extension is to be removed.
        """
        resource_client = getattr(self._confd, self.resource_confd)
        resource_client(resource).remove_extension(extension)
        self._confd.extensions.delete(extension)

    def _get_main_extension(self, resource):
        """
        Gets the main extension of a resource.

        Args:
            resource (dict): The resource containing extensions.

        Returns:
            dict: The main extension if it exists, otherwise None.
        """
        resource_id = resource.get('uuid', resource.get('id'))
        if not resource_id:
            logger.debug(
                'Unable to extract resource_id from %s resource', self.resource_confd
            )
            return None

        resource_client = getattr(self._confd, self.resource_confd)
        for extension in resource_client.get(resource_id).get('extensions', []):
            return extension
        return None


def get_extension_service(confd_client=Depends(get_accent_confd_client)):
    """
    Dependency for injecting BaseConfdExtensionService with ConfdClient.
    """
    service = BaseConfdExtensionService(confd_client)
    # Optionally set `resource_confd` dynamically
    service.resource_confd = "default_resource_name"  # Replace with your default resource
    return service
