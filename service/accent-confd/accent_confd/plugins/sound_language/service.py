# Copyright 2023 Accent Communications


class SoundLanguageService:
    def __init__(self, ari_client):
        self.ari_client = ari_client

    def search(self, parameters):
        result = self.ari_client.get_sounds_languages()
        return len(result), result


def build_service(ari_client):
    return SoundLanguageService(ari_client)
