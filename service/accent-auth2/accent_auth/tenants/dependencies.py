# accent_auth/tenants/dependencies.py

from typing import Annotated

from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from accent_auth.db import DAO
from accent_auth.db.engine import AsyncSessionLocal

# from accent_auth.utils.helpers import is_uuid  # Moved
from accent_auth.utils import is_uuid
from contextlib import asynccontextmanager
from .models import Tenant


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


async def valid_tenant_id(
    tenant_uuid: str,
    dao: DAO = Depends(DAO.from_defaults),
    db: AsyncSession = Depends(get_db),
) -> str:
    if not is_uuid(tenant_uuid):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid tenant_uuid format"
        )

    if not await dao.tenant.exists(tenant_uuid, session=db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found"
        )
    return tenant_uuid


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


class Permissions:
    TENANT_CREATE = Depends(is_admin)
    TENANT_READ = Depends(get_db)
    TENANT_UPDATE = Depends(valid_tenant_id)
    TENANT_DELETE = Depends(valid_tenant_id)
    TENANT_DOMAINS_READ = Depends(valid_tenant_id)
