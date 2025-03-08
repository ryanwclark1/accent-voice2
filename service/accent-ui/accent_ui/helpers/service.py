# Copyright 2023 Accent Communications


class BaseConfdService:
    resource_confd = None

    def list(
        self, limit=None, order=None, direction=None, offset=None, search=None, **kwargs
    ):
        resource_client = getattr(self._confd, self.resource_confd)
        return resource_client.list(
            search=search,
            order=order,
            limit=limit,
            direction=direction,
            offset=offset,
            **kwargs
        )

    def get(self, resource_id):
        resource_client = getattr(self._confd, self.resource_confd)
        return resource_client.get(resource_id)

    def update(self, resource):
        resource_client = getattr(self._confd, self.resource_confd)
        resource_client.update(resource)

    def create(self, resource):
        resource_client = getattr(self._confd, self.resource_confd)
        return resource_client.create(resource)

    def delete(self, resource_id):
        resource_client = getattr(self._confd, self.resource_confd)
        resource_client.delete(resource_id)
