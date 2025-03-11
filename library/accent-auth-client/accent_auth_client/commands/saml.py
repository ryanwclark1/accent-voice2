# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import cast

import httpx
from accent_lib_rest_client import RESTCommand

from accent_auth_client.type_definitions import ACSRedirectLocation, LogoutRedirectLocation, SSOResponseDict

logger = logging.getLogger(__name__)


class SAMLCommand(RESTCommand):
    """Command for SAML-related operations.

    Provides methods for SAML authentication flows.
    """

    resource = "saml"

    async def sso_async(self, domain: str, redirect_url: str) -> SSOResponseDict:
        """Initiate SSO flow asynchronously.

        Args:
            domain: Domain name
            redirect_url: Redirect URL after authentication

        Returns:
            SSOResponseDict: SSO response information

        Raises:
            AccentAPIError: If the request fails

        """
        data = {"redirect_url": redirect_url, "domain": domain}
        headers = self._get_headers()
        url = f"{self.base_url}/sso"

        r = await self.async_client.post(url, headers=headers, json=data)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("SSO request failed for domain: %s", domain)
            self.raise_from_response(r)

        return cast(SSOResponseDict, r.json())

    def sso(self, domain: str, redirect_url: str) -> SSOResponseDict:
        """Initiate SSO flow.

        Args:
            domain: Domain name
            redirect_url: Redirect URL after authentication

        Returns:
            SSOResponseDict: SSO response information

        Raises:
            AccentAPIError: If the request fails

        """
        data = {"redirect_url": redirect_url, "domain": domain}
        headers = self._get_headers()
        url = f"{self.base_url}/sso"

        r = self.sync_client.post(url, headers=headers, json=data)

        if r.status_code != 200:
            logger.error("SSO request failed for domain: %s", domain)
            self.raise_from_response(r)

        return cast(SSOResponseDict, r.json())

    async def acs_async(
        self, saml_response: str, relay_state: str
    ) -> ACSRedirectLocation:
        """Process SAML Assertion Consumer Service response asynchronously.

        Args:
            saml_response: SAML response
            relay_state: Relay state

        Returns:
            ACSRedirectLocation: Redirect location

        Raises:
            AccentAPIError: If the request fails

        """
        data = {"RelayState": relay_state, "SAMLResponse": saml_response}
        headers = self._get_headers()
        url = f"{self.base_url}/acs"

        r = await self.async_client.post(
            url, headers=headers, data=data, follow_redirects=False
        )

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("ACS request failed")
            self.raise_from_response(r)

        if r.status_code != 302:
            logger.error("Expected redirect status 302, got %s", r.status_code)
            self.raise_from_response(r)

        return cast(ACSRedirectLocation, r.headers["Location"])

    def acs(self, saml_response: str, relay_state: str) -> ACSRedirectLocation:
        """Process SAML Assertion Consumer Service response.

        Args:
            saml_response: SAML response
            relay_state: Relay state

        Returns:
            ACSRedirectLocation: Redirect location

        Raises:
            AccentAPIError: If the request fails

        """
        data = {"RelayState": relay_state, "SAMLResponse": saml_response}
        headers = self._get_headers()
        url = f"{self.base_url}/acs"

        r = self.sync_client.post(
            url, headers=headers, data=data, follow_redirects=False
        )

        if r.status_code != 302:
            logger.error("Expected redirect status 302, got %s", r.status_code)
            self.raise_from_response(r)

        return cast(ACSRedirectLocation, r.headers["Location"])

    async def logout_async(self) -> LogoutRedirectLocation:
        """Initiate logout flow asynchronously.

        Returns:
            LogoutRedirectLocation: Logout redirect location

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/logout"

        r = await self.async_client.get(url, headers=headers, follow_redirects=False)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Logout request failed")
            self.raise_from_response(r)

        return cast(LogoutRedirectLocation, r.json()["Location"])

    def logout(self) -> LogoutRedirectLocation:
        """Initiate logout flow.

        Returns:
            LogoutRedirectLocation: Logout redirect location

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/logout"

        r = self.sync_client.get(url, headers=headers, follow_redirects=False)

        if r.status_code != 200:
            logger.error("Logout request failed")
            self.raise_from_response(r)

        return cast(LogoutRedirectLocation, r.json()["Location"])
