# Copyright 2023 Accent Communications

from accent_auth import BaseMetadata


class DefaultExternalAPI(BaseMetadata):
    def get_token_metadata(self, login, args):
        metadata = super().get_token_metadata(login, args)
        metadata.update(purpose='external_api')
        return metadata
