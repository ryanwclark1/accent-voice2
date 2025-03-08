# accent_auth/auth/permissions.py
from typing import Annotated

from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from accent_auth.db import DAO
from accent_auth.db.engine import AsyncSessionLocal

# from accent_auth.utils.helpers import is_uuid  # Moved
from accent_auth.utils import is_uuid
from contextlib import asynccontextmanager
from accent_auth.services.user import UserService


async def get_db() -> AsyncSession:
    """Dependency that provides a new async database session per request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def valid_token(
    token: str = Header(...),
    dao: DAO = Depends(DAO.from_defaults),
    db: AsyncSession = Depends(get_db),
):
    try:
        # Assuming your DAO has a method to get token data
        return await dao.token.get(token, session=db)
    except Exception:  # Replace with your specific exception for invalid tokens
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


async def is_admin(
    user_service: UserService = Depends(UserService),
    db: AsyncSession = Depends(get_db),
    token: str = Header(...),
) -> None:
    """Dependency to check if the user has the 'admin' role."""
    token_data = await valid_token(token, db=db)
    try:
        user = await user_service.get_user(token_data.auth_id, db=db)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not user or "admin" not in (user.get("roles") or []):  # Check for 'admin' role
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return


async def valid_policy_id(
    policy_uuid: str,
    dao: DAO = Depends(DAO.from_defaults),
    db: AsyncSession = Depends(get_db),
) -> str:
    if not is_uuid(policy_uuid):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid policy_uuid format"
        )

    if not await dao.policy.exists(policy_uuid, session=db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found"
        )
    return policy_uuid


async def valid_group_id(
    group_uuid: str,
    dao: DAO = Depends(DAO.from_defaults),
    db: AsyncSession = Depends(get_db),
) -> str:
    if not is_uuid(group_uuid):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid group_uuid format"
        )

    if not await dao.group.exists(group_uuid, session=db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group not found"
        )
    return group_uuid


class Permissions:
    # TOKEN_CREATE = Depends(get_db)  # Example: Any valid DB connection = can create
    TOKEN_READ = Depends(valid_token)
    TOKEN_DELETE = Depends(valid_token)
    BACKEND_READ = Depends(get_db)  # Example: Any valid DB connection
    BACKEND_LDAP_READ = Depends(get_db)
    BACKEND_LDAP_UPDATE = Depends(get_db)
    BACKEND_LDAP_DELETE = Depends(get_db)
    BACKEND_SAML_READ = Depends(get_db)
    BACKEND_SAML_CREATE = Depends(get_db)
    BACKEND_SAML_UPDATE = Depends(get_db)
    BACKEND_SAML_DELETE = Depends(get_db)
    SAML_ACS = Depends(get_db)
    EXTERNAL_AUTH = Depends(get_db)
    CONFIG_READ = Depends(is_admin)
    CONFIG_UPDATE = Depends(is_admin)
    POLICY_CREATE = Depends(is_admin)
    POLICY_READ = Depends(get_db)
    POLICY_UPDATE = Depends(valid_policy_id)
    POLICY_DELETE = Depends(valid_policy_id)
    GROUP_CREATE = Depends(is_admin)
    GROUP_READ = Depends(get_db)
    GROUP_UPDATE = Depends(valid_group_id)
    GROUP_DELETE = Depends(valid_group_id)
    GROUP_POLICY_CREATE = (Depends(valid_group_id), Depends(valid_policy_id))
    GROUP_POLICY_DELETE = (Depends(valid_group_id), Depends(valid_policy_id))
    GROUP_POLICY_READ = Depends(valid_group_id)
    GROUP_USER_READ = Depends(valid_group_id)
    GROUP_USER_CREATE = (Depends(valid_group_id), Depends(valid_user_id))
    GROUP_USER_DELETE = (Depends(valid_group_id), Depends(valid_user_id))
    USER_CREATE = Depends(get_db)  # Example: Any valid DB connection = can create.
    USER_READ = Depends(get_db)  # Requires a valid user ID.
    USER_UPDATE = Depends(valid_user_id)  # Requires a valid user ID.
    USER_DELETE = Depends(valid_user_id)  # Requires a valid user ID.
    USER_EMAIL_CONFIRM = Depends(valid_email_id)
    USER_SESSION_READ = Depends(valid_user_id)
    USER_SESSION_DELETE = (
        Depends(valid_user_id),
        Depends(valid_session_id),
    )  # Requires both user and session.
    TENANT_CREATE = Depends(is_admin)
    TENANT_READ = Depends(get_db)
    TENANT_UPDATE = Depends(valid_tenant_id)
    TENANT_DELETE = Depends(valid_tenant_id)
    TENANT_DOMAINS_READ = Depends(valid_tenant_id)
