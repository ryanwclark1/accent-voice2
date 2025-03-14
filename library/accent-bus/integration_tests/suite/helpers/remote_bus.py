# Copyright 2023 Accent Communications

import requests


class RemoteBusApiClient:
    def __init__(self, host="127.0.0.1", port=5000) -> None:
        self._base_url = f"http://{host}:{port}"

    def _make_url(self, *part):
        return "/".join([self._base_url, *part])

    def subscribe(self, event, headers=None, headers_match_all=True, routing_key=None):
        url = self._make_url("bus", event, "subscribe")
        payload = {
            "headers": headers,
            "headers_match_all": headers_match_all,
            "routing_key": routing_key,
        }
        resp = requests.post(url, json=payload)
        return resp.status_code == 200

    def unsubscribe(
        self, event, headers=None, headers_match_all=True, routing_key=None
    ):
        url = self._make_url("bus", event, "unsubscribe")
        payload = {
            "headers": headers,
            "headers_match_all": headers_match_all,
            "routing_key": routing_key,
        }
        resp = requests.post(url, json=payload)
        return resp.status_code == 200

    def publish(self, event, payload=None, headers=None, routing_key=None):
        url = self._make_url("bus", event, "publish")
        payload = {"headers": headers, "routing_key": routing_key, "payload": payload}
        resp = requests.post(url, json=payload)
        return resp.status_code == 200

    def get_messages(self, event):
        url = self._make_url("bus", event, "messages")
        return requests.get(url).json()

    def get_messages_count(self, event):
        url = self._make_url("bus", event, "messages", "count")
        return requests.get(url).json()

    def get_status(self):
        url = self._make_url("bus", "status")
        return requests.get(url).json()
