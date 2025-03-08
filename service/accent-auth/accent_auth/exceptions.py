# accent_auth/exceptions.py

from fastapi import HTTPException, status  # Import from FastAPI
from typing import Any


class BaseAPIException(HTTPException):  # Inherit from HTTPException
    """Base class for API exceptions."""

    def __init__(
        self,
        status_code: int,
        message: str,
        error_id: str,  # Add an error_id for machine-readable errors
        details: dict[str, Any] | None = None,
        resource: str | None = None,  # The resource type (e.g., "users", "tokens")
        headers: dict[str, Any] | None = None,  # For headers
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "error_id": error_id,
                "resource": resource,
                "details": details or {},
            },
            headers=headers,
        )


class ConflictException(BaseAPIException):
    """Exception raised for conflicts (HTTP 409)."""

    def __init__(self, resource: str, column: str, value: Any):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=f"Conflict detected on {resource}",
            error_id="conflict",
            details={
                column: {
                    "constraint_id": "unique",
                    "message": f"{value} already present",
                }
            },
            resource=resource,
        )


class InvalidLimitException(BaseAPIException):
    def __init__(self, limit):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Invalid limit.",
            error_id="invalid-limit",
            details={"limit": str(limit)},
        )


class InvalidOffsetException(BaseAPIException):
    def __init__(self, offset):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Invalid offset.",
            error_id="invalid-offset",
            details={"offset": str(offset)},
        )


class InvalidSortColumnException(BaseAPIException):
    def __init__(self, column):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Invalid sort column.",
            error_id="invalid-sort-column",
            details={"column": column},
        )


class InvalidSortDirectionException(BaseAPIException):
    def __init__(self, direction):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Invalid sort direction.",
            error_id="invalid-sort-direction",
            details={"direction": direction},
        )


class TopTenantNotInitialized(BaseAPIException):
    def __init__(self):
        msg = "accent-auth top tenant is not initialized"
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message=msg,
            error_id="top-tenant-not-initialized",
        )


class TokenServiceException(Exception):
    pass


class InvalidTokenException(TokenServiceException):
    """Exception raised for invalid tokens."""

    pass


class MissingPermissionsTokenException(TokenServiceException):
    """Exception raised for missing permissions."""

    pass


class MaxConcurrentSessionsReached(TokenServiceException):
    """Exception raised when the maximum number of concurrent sessions is reached."""

    def __init__(self, user_uuid: str):
        super().__init__(
            f"User {user_uuid} has exceeded the maximum number of active sessions"
        )


class UnknownTokenException(TokenServiceException):
    """Exception raised for unknown tokens."""

    def __init__(self):
        super().__init__("No such token")


class DuplicatedSAMLConfigException(Exception):
    def __init__(self, tenant_uuid):
        self.tenant_uuid = tenant_uuid
        super().__init__(
            f"Duplicated SAML config for tenant_uuid {tenant_uuid}",
        )


class SAMLConfigParameterException(Exception):
    def __init__(self, tenant_uuid, msg, code):
        super().__init__(
            f"SAML configuration error for tenant {tenant_uuid}: {msg} ({code})"
        )
        self.tenant_uuid = tenant_uuid
        self.msg = msg
        self.code = code


class UnknownSAMLConfigException(Exception):
    def __init__(self, tenant_uuid):
        super().__init__(f"Unknown SAML config for tenant {tenant_uuid}")
        self.tenant_uuid = tenant_uuid


class NoSuchBackendException(Exception):
    def __init__(self, backend_name):
        super().__init__(f"no such backend {backend_name}")


class InvalidUsernamePassword(Exception):
    def __init__(self, login):
        super().__init__(f"unknown username or password for login {login}")


class NoMatchingSAMLSession(Exception):
    def __init__(self, saml_session_id):
        super().__init__(f"unknown saml_session_id {saml_session_id}")


class UnauthorizedAuthenticationMethod(Exception):
    def __init__(self, authorized_authentication_method):
        super().__init__(
            f"unauthorized authentication method should use {authorized_authentication_method}"
        )


class DuplicatedRefreshTokenException(Exception):
    def __init__(self, user_uuid, client_id):
        self.client_id = client_id
        self.user_uuid = user_uuid
        super().__init__(
            f"Duplicated Refresh Token for user_uuid {user_uuid} and client_id {client_id}",
        )


class UnknownRefreshToken(Exception):
    def __init__(self, client_id):
        super().__init__(f'unknown refresh_token for client_id "{client_id}"')


class UnknownRefreshTokenUUID(Exception):
    def __init__(self, uuid):
        super().__init__(f'unknown refresh_token uuid "{uuid}"')


class SAMLException(Exception):
    pass


class SAMLConfigurationError(SAMLException):
    def __init__(self, domain, message=None):
        super().__init__(message or "SAML client for domain not found or failed")
        self.domain = domain


class SAMLProcessingError(SAMLException):
    pass


class SAMLProcessingErrorWithReturnURL(SAMLException):
    def __init__(self, error: str, return_url: str, code: int = 500):
        super().__init__(f"SAML processing failed: {error}")
        self.redirect_url = f"{return_url}?login_failure_code={code}"


class UnknownEmailException(Exception):
    def __init__(self, email_uuid):
        super().__init__(f'No such email: "{email_uuid}"')


class UnknownGroupException(Exception):
    def __init__(self, group_uuid):
        super().__init__(f'No such group: "{group_uuid}"')


class UnknownPolicyException(Exception):
    def __init__(self, policy_uuid):
        super().__init__(f'No such policy: "{policy_uuid}"')


class SystemGroupForbidden(Exception):
    def __init__(self, group_uuid):
        super().__init__(f'Forbidden group modification: "{group_uuid}"')


class DuplicateGroupException(Exception):
    def __init__(self, name):
        super().__init__(f'Group "{name}" already exists')


class DuplicatePolicyException(Exception):
    def __init__(self, name):
        super().__init__(f'Policy "{name}" already exists')


class TenantParamException(Exception):
    @classmethod
    def from_errors(cls, errors):
        for field, infos in errors.items():
            if not isinstance(infos, list):
                infos = [infos]
            for info in infos:
                return cls(info["message"], {field: info})


class UnknownTenantException(Exception):
    def __init__(self, tenant_uuid):
        super().__init__(f'No such tenant: "{tenant_uuid}"')


class UnauthorizedTenantwithChildrenDelete(Exception):
    def __init__(self, tenant_uuid):
        super().__init__(
            f'Unauthorized delete of tenant : "{tenant_uuid}" ; '  # noqa: E702
            "since it has at least one child"
        )


class MasterTenantConflictException(Exception):
    pass


class UnauthorizedResourcesMutualAccessAttemptException(Exception):
    pass


class DomainAlreadyExistException(Exception):
    pass


class UserParamException(Exception):
    pass


class UnknownUserException(Exception):
    def __init__(self, identifier, details=None):
        super().__init__(f'No such user: "{identifier}"')


class UnknownUserUUIDException(Exception):  # Keep for consistency with other DAOs
    def __init__(self, user_uuid: str):
        super().__init__(f"No such user: {user_uuid}")


class UnknownLoginException(Exception):
    def __init__(self, login):
        super().__init__(f'No such user: "{login}"')


class PasswordIsManagedExternallyException(Exception):
    def __init__(self, user_uuid, details=None):
        super().__init__(
            f'Unable to update externally managed password for user : "{user_uuid}"'
        )


class ExternalAuthAlreadyExists(Exception):
    def __init__(self, auth_type):
        super().__init__(
            f'This external authentication method has already been set: "{auth_type}"'
        )


class ExternalAuthConfigAlreadyExists(Exception):
    def __init__(self, auth_type):
        super().__init__(
            f'This external authentication config has already been set: "{auth_type}"'
        )


class ExternalAuthConfigNotFound(Exception):
    def __init__(self, auth_type):
        super().__init__(
            f'Configuration for this external auth type "{auth_type}" is not defined.'
        )


class UnknownExternalAuthException(Exception):
    def __init__(self, auth_type):
        super().__init__(f'No such external auth: "{auth_type}"')


class UnknownExternalAuthConfigException(Exception):
    def __init__(self, auth_type):
        super().__init__(f'No config found for this external auth type: "{auth_type}"')


class UnknownExternalAuthTypeException(Exception):
    def __init__(self, auth_type):
        super().__init__(f'No such auth type: "{auth_type}"')


class UsernameLoginAlreadyExists(ConflictException):
    def __init__(self, username):
        super().__init__("users", "username", username)


class EmailLoginAlreadyExists(ConflictException):
    def __init__(self, email):
        super().__init__("users", "email_address", email)


class AuthenticationFailedException(Exception):
    code = 401
    _msg = "Authentication Failed"

    def __str__(self):
        return self._msg


class InvalidListParamException(Exception):
    pass
