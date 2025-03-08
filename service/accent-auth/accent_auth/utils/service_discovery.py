# accent_auth/utils/service_discovery.py

import logging

import httpx
from accent_auth.config.app import settings

logger = logging.getLogger(__name__)


async def self_check() -> bool:
    """Performs a self-check by making an HTTP request to the /backends endpoint.

    This function is intended to be used with a service discovery system
    (like Consul) to determine if the service is healthy.

    Returns:
        bool: True if the self-check was successful, False otherwise.
    """
    scheme = (
        "https"
        if settings.rest_api["certificate"] and settings.rest_api["private_key"]
        else "http"
    )
    host = "localhost"  # Access settings correctly
    port = settings.rest_api["port"]
    endpoint = "backends"
    url = f"{scheme}://{host}:{port}/0.1/{endpoint}"
    headers = {"accept": "application/json"}
    timeout = httpx.Timeout(5.0, connect=5.0)  # Explicit timeout

    try:
        async with httpx.AsyncClient(verify=False, timeout=timeout) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return True  # If we get here, the request was successful
    except httpx.RequestError as e:  # Catch specific httpx exceptions
        logger.warning("Self-check failed (request error): %s", e)
        return False
    except httpx.HTTPStatusError as e:  # Catch HTTP errors (like 404, 500)
        logger.warning("Self-check failed (HTTP status error): %s", e)
        return False
    except Exception as e:  # Catch any other unexpected exceptions
        logger.exception("Self-check failed (unexpected error): %s", e)
        return False
