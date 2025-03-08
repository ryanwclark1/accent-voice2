# accent_auth/auth/routes.py
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Header, Form, Query
from accent_auth.auth.service import AuthenticationService

from accent_auth.db.engine import AsyncSessionLocal
from accent_auth.services.saml import SAMLService
from accent_auth.services.ldap import LDAPService

from accent_auth.db import DAO
from accent_auth.dependencies import get_db
from accent_auth.services.token import TokenService
from accent_auth.auth.permissions import Permissions
from accent_auth import exceptions
from .schemas import (
    TokenRequest,
    TokenResponse,
    TokenScopesCheckRequest,
    TokenScopesCheckResponse,
    RefreshTokenList,
    SAMLLoginContext,
    SAMLSSOResponse,
    SAMLIdpResponse,
    SAMLLogoutRequest,
    ExternalAuthConfig,
    ExternalAuthUser,
    ExternalAuthUserList,
    IDPList
)
from fastapi.responses import RedirectResponse, Response
from .external import google, microsoft, mobile

logger = logging.getLogger(__name__)

router = APIRouter()
auth_router = APIRouter(
    prefix="/tokens",
    tags=["tokens"],
    responses={404: {"description": "Not found"}},
)
# Added a default response model in case of a 401.
no_auth_router = APIRouter(
    prefix="/tokens",
    tags=["tokens"],
)
# Include external auth routes
router.include_router(google.router)
router.include_router(microsoft.router)
router.include_router(mobile.router)

@no_auth_router.post("/", response_model=TokenResponse)  # Use response_model
async def create_token(
    token_request: TokenRequest,
    dao: DAO = Depends(DAO.from_defaults),
    auth_service: AuthenticationService = Depends(AuthenticationService),
    db: AsyncSession = Depends(get_db)
):
    """Creates a new authentication token."""
    try:
        backend, login = await auth_service.verify_auth(token_request.model_dump(), session=db)
    except exceptions.TokenServiceException as e:  # More specific exception handling
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except exceptions.InvalidUsernamePassword as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    #TODO get args
    args = {}
    token = await dao.token_service.new_token(backend, login, args, session=db)  # Assuming new_token is async
    return token  # FastAPI automatically converts this to JSON


@router.get(
    "/{token}", response_model=TokenResponse, dependencies=[Depends(Permissions.TOKEN_READ)]
)
async def get_token(
    token: str,
    required_access: str | None = None,
    tenant: str | None = None,
    token_service: TokenService = Depends(TokenService),
    db: AsyncSession = Depends(get_db)
):
    """Retrieves token data. Checks for required access and tenant if provided."""
    try:
        token_data = await token_service.get(token, required_access, db=db)
        await token_service.assert_has_tenant_permission(token_data.model_dump(), tenant, db=db) #Added to dict
        return token_data
    except exceptions.TokenServiceException as e:  # More specific exception handling
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except exceptions.MissingPermissionsTokenException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    except exceptions.MissingTenantTokenException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

@router.head(
    "/{token}",  dependencies=[Depends(Permissions.TOKEN_READ)], status_code=204
)
async def check_token(
    token: str,
    required_access: str | None = None,
    tenant: str | None = None,
    token_service: TokenService = Depends(TokenService),
    db: AsyncSession = Depends(get_db)
    ):
    """Checks if a token is valid."""
    try:
        token_data = await token_service.get(token, required_access, db=db)
        await token_service.assert_has_tenant_permission(token_data.model_dump(), tenant, db=db)  #Added to dict
    except exceptions.TokenServiceException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except exceptions.MissingAccessTokenException:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    except exceptions.MissingTenantTokenException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete(
    "/{token}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(Permissions.TOKEN_DELETE)]
)
async def revoke_token(token: str,  token_service: TokenService = Depends(TokenService), db: AsyncSession = Depends(get_db)):
    """Revokes (deletes) a token."""
    await token_service.remove_token(token, db=db)
    return  # Return nothing for 204 NO CONTENT


@router.post(
    "/{token}/scopes/check",
    response_model=TokenScopesCheckResponse,
)
async def check_token_scopes(
    token: str,
    request: TokenScopesCheckRequest,
    token_service: TokenService = Depends(TokenService),
    db: AsyncSession = Depends(get_db)
) -> TokenScopesCheckResponse:
    """Checks a token against a list of scopes."""
    try:
        token_data, scopes_statuses = await token_service.check_scopes(
            token, request.scopes, db=db
        )
        await token_service.assert_has_tenant_permission(
            token_data.model_dump(), request.tenant_uuid, db=db
        )
        return TokenScopesCheckResponse(scopes=scopes_statuses)
    except exceptions.TokenServiceException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except exceptions.MissingTenantTokenException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

@router.get("/", response_model=RefreshTokenList)
async def list_refresh_tokens(token_service: TokenService = Depends(TokenService), db: AsyncSession = Depends(get_db)):
    """Lists all refresh tokens."""
    refresh_tokens = await token_service.list_refresh_tokens(db=db)
    return {"items": refresh_tokens, "total": len(refresh_tokens), "filtered": len(refresh_tokens)}

@router.post("/saml/sso", response_model=SAMLSSOResponse)
async def saml_sso(
    saml_login_context: SAMLLoginContext,
    saml_service: SAMLService = Depends(SAMLService),
    db: AsyncSession = Depends(get_db)
):
    """Creates and returns context and redirects to IdP login page."""
    try:
        location, saml_session_id = await saml_service.prepare_redirect_response(
            saml_login_context.redirect_url,
            saml_login_context.domain,
            db=db
        )
        return {"location": location, "saml_session_id": saml_session_id}
    except exceptions.SAMLConfigurationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except exceptions.SAMLProcessingError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        logger.exception("Failed to process initial SAML SSO post: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error during SAML SSO initialization",
        )


@router.post("/saml/acs")
async def saml_acs(
    RelayState: str = Form(...),
    SAMLResponse: str = Form(...),
    saml_service: SAMLService = Depends(SAMLService),
    db: AsyncSession = Depends(get_db)
):

    """Processes the IdP response and redirects to requested URL."""
    try:
        response_url = await saml_service.process_auth_response(
            request.url, request.client.host, {"RelayState": RelayState, "SAMLResponse": SAMLResponse}, db=db
        )
        return RedirectResponse(response_url)  # Use RedirectResponse
    except exceptions.SAMLProcessingErrorWithReturnURL as e:
        logger.info("SAML SSO answer processing failed, redirect with error")
        return RedirectResponse(e.redirect_url)  # Use RedirectResponse
    except exceptions.SAMLProcessingError as e:
        logger.warning("SAML SSO answer processing failed")
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        logger.exception("SAML unexpected error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/saml/logout")
async def saml_logout(
    saml_service: SAMLService = Depends(SAMLService),
    token_service: TokenService = Depends(TokenService),
    token: str = Depends(extract_token_id_from_header)
):
    """Initiates SAML logout."""
    try:
        token_data = await token_service.get(token, required_access=None)

        location = await saml_service.process_logout_request(
            token_data,
        )

        await token_service.remove_token(token)
        if refresh_token := token_data.refresh_token_uuid: #Added the missing colon
            await token_service.delete_refresh_token_by_uuid(refresh_token)

        return {"location": location}  # Return the redirect URL
    except exceptions.SAMLException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception("SAML logout failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/saml/sls")
async def saml_sls(
    SAMLResponse: str = Query(...),
    RelayState: str = Query(...),
    saml_service: SAMLService = Depends(SAMLService),
    db: AsyncSession = Depends(get_db)
):
    """Handles the logout response from the IDP."""
    try:
        location = await saml_service.process_logout_request_response(
            SAMLResponse, RelayState, binding=BINDING_HTTP_REDIRECT, db=db
        )
        return RedirectResponse(location)  # Use RedirectResponse
    except Exception as e:
        logger.exception("SAML logout response processing failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process logout request response",
        )

@router.get("/backends", response_model=list[str])  #  response model
async def list_backends(
    backends: BackendsProxy = Depends(lambda: BackendsProxy()) # We could improve this
):
    """Retrieves the list of activated backends."""
    # The logic to get the enabled backends will need to be adapted.
    # We can't directly access app.config['loaded_plugins'] anymore.
    # We might need to inject the enabled_backend_plugins setting, or
    # provide a method on the BackendsProxy to get the names. For now,
    # I'll use a placeholder.
    return list(backends._backends.keys())

@router.get("/backends/ldap", response_model=LDAPConfigSchema)
async def get_ldap_config(
    ldap_service: LDAPService = Depends(LDAPService),
    db: AsyncSession = Depends(get_db)
):
    """Retrieves the LDAP configuration for the current tenant."""
    try:
        tenant_uuid = "current_tenant" # replace by dependency
        return await ldap_service.get(tenant_uuid, db=db)
    except exceptions.UnknownLDAPConfigException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.exception("Failed to get LDAP config: %s", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/backends/ldap", response_model=LDAPConfigSchema)
async def update_ldap_config(
    config_update: LDAPConfigUpdateSchema,
    ldap_service: LDAPService = Depends(LDAPService),
    db: AsyncSession = Depends(get_db)
):
    """Updates the LDAP configuration for the current tenant."""
    try:
        tenant_uuid = "current_tenant" #Replace
        updated_config = await ldap_service.update(
            tenant_uuid, config_update.model_dump(exclude_none=True), db=db
        )  # Pass updated fields
        return updated_config
    except Exception as e:
        logger.exception("Failed to update LDAP config: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update LDAP config"
        )


@router.delete("/backends/ldap", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ldap_config(
    ldap_service: LDAPService = Depends(LDAPService),
    db: AsyncSession = Depends(get_db)
):
    """Deletes the LDAP configuration for the current tenant."""
    try:
        tenant_uuid = "current_tenant" #Replace
        await ldap_service.delete(tenant_uuid, db=db)
    except Exception as e:
        logger.exception("Failed to delete LDAP config: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return  # 204 No Content

@router.get("/backends/saml", response_model=SAMLConfigSchema)
async def get_saml_config(
    saml_config_service: SAMLConfigService = Depends(SAMLConfigService),
    db: AsyncSession = Depends(get_db)

):
    """Retrieves the SAML configuration for the current tenant."""
    try:
        tenant_uuid = "current_tenant"
        return await saml_config_service.get(tenant_uuid, db=db)
    except exceptions.UnknownSAMLConfigException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.exception("Failed to get SAML config: %s", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/backends/saml", response_model=SAMLConfigSchema, status_code=201)
async def create_saml_config(
    metadata: UploadFile = File(...),
    domain_uuid: str = Form(...),
    entity_id: str = Form(...),
    acs_url: str = Form(...),
    saml_config_service: SAMLConfigService = Depends(SAMLConfigService),
    db: AsyncSession = Depends(get_db)
):
    """Creates a new SAML configuration for the current tenant."""
    try:
        tenant_uuid = "current_tenant"
        idp_metadata = ElementTree.parse(metadata.file)
        config_data = {
            "tenant_uuid": tenant_uuid,
            "domain_uuid": domain_uuid,
            "entity_id": entity_id,
            "idp_metadata": idp_metadata,
            "acs_url": acs_url
        }

        result = await saml_config_service.create(db=db, **config_data)
        return result
    except exceptions.DuplicatedSAMLConfigException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except Exception as e:
        logger.exception("Failed to create SAML config: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.put("/backends/saml", response_model=SAMLConfigSchema)
async def update_saml_config(
    metadata: UploadFile = File(None),  # Metadata is optional for updates
    domain_uuid: str | None = Form(None),
    entity_id: str | None = Form(None),
    acs_url: str | None = Form(None),
    saml_config_service: SAMLConfigService = Depends(SAMLConfigService),
    db: AsyncSession = Depends(get_db)
):
    """Updates the SAML configuration for the current tenant."""
    tenant_uuid = "current_tenant" # Replace

    update_data = {}
    if domain_uuid:
        update_data["domain_uuid"] = domain_uuid
    if entity_id:
        update_data["entity_id"] = entity_id
    if acs_url:
        update_data["acs_url"] = acs_url
    if metadata:
         try:
             update_data["idp_metadata"] = ElementTree.parse(metadata.file)
         except ElementTree.ParseError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid XML ({e})"
            )
    try:
        result = await saml_config_service.update(tenant_uuid, db=db, **update_data)
        return result
    except Exception as e:
        logger.exception("Failed to update SAML config: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.delete("/backends/saml", status_code=status.HTTP_204_NO_CONTENT)
async def delete_saml_config(
    saml_config_service: SAMLConfigService = Depends(SAMLConfigService),
    db: AsyncSession = Depends(get_db)
):
    """Deletes the SAML configuration for the current tenant."""
    tenant_uuid = "current_tenant" #Replace
    try:
        await saml_config_service.delete(tenant_uuid, db=db)
    except Exception as e:
        logger.exception("Failed to delete SAML config: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return  # 204 No Content


@router.get("/backends/saml/metadata")
async def get_saml_metadata(saml_config_service: SAMLConfigService = Depends(SAMLConfigService), db: AsyncSession = Depends(get_db)):
    """Downloads the tenant SAML metadata XML file."""
    tenant_uuid = "current_tenant" # Replace
    try:
        etree_metadata = await saml_config_service.get_metadata(tenant_uuid, db=db)
        # Convert ElementTree to string representation
        xml_string = ElementTree.tostring(etree_metadata, encoding="utf-8").decode()
        return Response(content=xml_string, media_type="application/xml")

    except exceptions.UnknownSAMLConfigException:
        raise HTTPException(status_code=404, detail='No SAML SP metadata available for this tenant')

    except Exception as e:
        logger.exception("Failed to get SAML metadata: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

@router.get("/backends/saml/acs_url_template")
async def get_saml_acs_url_template(saml_config_service: SAMLConfigService = Depends(SAMLConfigService)):
    try:
        url = await saml_config_service.get_acs_url_template()
        return {"acs_url": url}
    except exceptions.UnknownSAMLConfigException as e:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.exception("Failed to get SAML ACS URL template: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

@router.get("/idp", response_model=IDPList)
async def list_idp_types(idp_service: IDPService = Depends(IDPService), db: AsyncSession = Depends(get_db)):
    """Retrieves the list of valid identity provider types."""
    return {"types": await idp_service.list(db=db)}


@router.put("/idp/{idp_type}/users/{user_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def add_user_idp(
    idp_type: str,
    user_uuid: str = Depends(valid_user_id),
    idp_service: IDPService = Depends(IDPService),
    db: AsyncSession = Depends(get_db)
):
    """Associate multiple users to a IDP"""
    await idp_service.add_user(idp_type, user_uuid, db=db)
    return


@router.delete("/idp/{idp_type}/users/{user_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user_idp(
    idp_type: str,
    user_uuid: str = Depends(valid_user_id),
    idp_service: IDPService = Depends(IDPService),
    db: AsyncSession = Depends(get_db)
):
    """Dissociate a user from an IDP"""
    await idp_service.remove_user(idp_type, user_uuid, db=db)
    return
class ExternalAuthConfig(BaseModel):
    data: dict
    type_uuid: str
    tenant_uuid: str

class ExternalAuthUser(BaseModel):
     uuid: str

class ExternalAuthUserList(BaseModel):
    total: int
    filtered: int
    items: list[ExternalAuthUser]

@router.get("/external/{auth_type}/config", response_model=ExternalAuthConfig)
async def get_external_auth_config(
    auth_type: str,
    external_auth_service: ExternalAuthService = Depends(ExternalAuthService),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve the configuration for a specific external auth provider."""
    try:
        tenant_uuid = "current_tenant" #Replace
        config = await external_auth_service.get_config(auth_type, tenant_uuid, db=db)  # Need to update service
        return config
    except Exception as e:  # Replace with your specific exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/external/{auth_type}/config",
    response_model=ExternalAuthConfig,
    status_code=status.HTTP_201_CREATED,
)
async def create_external_auth_config(
    auth_type: str,
    config: ExternalAuthConfig,
    external_auth_service: ExternalAuthService = Depends(ExternalAuthService),
    db: AsyncSession = Depends(get_db)
):
    """Create configuration for an external auth provider."""
    try:
        tenant_uuid = "current_tenant"
        created_config =