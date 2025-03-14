# Copyright 2023 Accent Communications

from __future__ import annotations

import contextlib
import json
import logging
from typing import Any, TypedDict

# TODO(sileht): move the http plugin to httpx too.
import httpx
import requests

logger = logging.getLogger(__name__)


class RequestDetailsDict(TypedDict):
    request_method: str
    request_url: str
    request_body: dict[str, str] | str | None
    request_headers: dict[str, str]
    response_status_code: int | None
    response_headers: dict[str, str]
    response_body: dict[str, str] | str | None


class ErrorRequestDetailsDict(RequestDetailsDict):
    error: str


class HookExpectedError(Exception):
    def __init__(self, detail: ErrorRequestDetailsDict | str | dict[str, Any]) -> None:
        self.detail = detail
        super().__init__()


class HookRetry(Exception):
    def __init__(self, detail: ErrorRequestDetailsDict | str | dict[str, Any]) -> None:
        self.detail = detail
        super().__init__()


def _decode(data: str | bytes | None) -> str | dict[str, Any] | None:
    if data is None:
        return None

    if isinstance(data, bytes):
        text = data.decode()
    else:
        text = data

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


@contextlib.contextmanager
def requests_automatic_hook_retry(task):
    try:
        yield
    except (requests.exceptions.HTTPError, httpx.HTTPError) as exc:
        if exc.request is None or exc.response is None:
            raise ValueError('No request/response in error object')
        if isinstance(exc.request, requests.PreparedRequest):
            req_data = exc.request.body
        elif isinstance(exc.request, httpx.Request):
            exc.request.read()  # to be removed in Debian 12 Bookworm with httpx==0.23.3
            req_data = exc.request.content  # type: ignore
        if exc.response.status_code == 410:
            logger.info(
                "http request fail, service is gone (%d/%d): '%s %s [%s]' %s",
                task.request.retries,
                task.max_retries,
                exc.request.method,
                exc.request.url,
                exc.response.status_code,
                _decode(exc.response.text),
            )
            raise HookExpectedError(
                {
                    "error": str(exc),
                    "request_method": str(exc.request.method),
                    "request_url": str(exc.request.url),
                    "request_body": _decode(req_data),
                    "request_headers": dict(exc.request.headers),
                    "response_status_code": exc.response.status_code,
                    "response_headers": dict(exc.response.headers),
                    "response_body": _decode(exc.response.text),
                }
            )
        else:
            logger.info(
                "http request fail, retrying (%s/%s): '%s %s [%s]' %s",
                task.request.retries,
                task.max_retries,
                exc.request.method,
                exc.request.url,
                exc.response.status_code,
                _decode(exc.response.text),
            )
            raise HookRetry(
                {
                    "error": str(exc),
                    "request_method": str(exc.request.method),
                    "request_url": str(exc.request.url),
                    "request_body": _decode(req_data),
                    "request_headers": dict(exc.request.headers),
                    "response_status_code": exc.response.status_code,
                    "response_headers": dict(exc.response.headers),
                    "response_body": _decode(exc.response.text),
                }
            )

    except (
        httpx.TimeoutException,
        httpx.TooManyRedirects,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.TooManyRedirects,
    ) as exc:
        request: requests.PreparedRequest | httpx.Request = exc.request  # type: ignore
        logger.info(
            "http request fail, retrying (%s/%s): '%s %s [%s]'",
            task.request.retries,
            task.max_retries,
            request.method,
            request.url,
            exc,
        )
        if isinstance(request, requests.PreparedRequest):
            req_data = request.body
        else:
            req_data = request.content
        raise HookRetry(
            {
                "error": str(exc),
                "request_method": str(request.method),
                "request_url": str(request.url),
                "request_body": _decode(req_data),
                "request_headers": dict(request.headers),
                "response_status_code": None,
                "response_headers": {},
                "response_body": "",
            }
        )


def requests_automatic_detail(
    response: httpx.Response | requests.Response,
) -> RequestDetailsDict:
    if isinstance(response.request, requests.PreparedRequest):
        req_data = response.request.body
    else:
        req_data = response.request.read()
    return {
        "request_method": response.request.method,
        "request_url": str(response.request.url),
        "request_body": _decode(req_data),
        "request_headers": dict(response.request.headers),
        "response_status_code": response.status_code,
        "response_headers": dict(response.headers),
        "response_body": _decode(response.text),
    }
