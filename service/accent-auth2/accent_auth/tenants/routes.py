# accent_auth/tenants/routes.py

import logging

from fastapi import APIRouter, Depends, HTTPException, status

# from accent_auth.db.engine import AsyncSessionLocal  # REMOVED
from accent_auth.services.tenant import TenantService

# from accent_auth.auth.permissions import Permissions # Removed for now, no permissions.
from .dependencies import (
    Permissions,
    valid_tenant_id,
)  # Import Permissions and validation
from . import schemas
from accent_auth import exceptions
from accent_auth.dependencies import get_db  # Import the session dependency
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tenants",
    tags=["tenants"],
)


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


@router.post(
    "/",
    response_model=schemas.TenantResult,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(Permissions.TENANT_CREATE)],
)
async def create_tenant(
    tenant: schemas.TenantCreate,
    tenant_service: TenantService = Depends(TenantService),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await tenant_service.create(db=db, **tenant.model_dump())
    except exceptions.MasterTenantConflictException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except exceptions.DuplicateTenantException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.exception("Failed to create tenant: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create tenant",
        )


@router.get(
    "/",
    response_model=schemas.TenantList,
    dependencies=[Depends(Permissions.TENANT_READ)],
)
async def list_tenants(
    tenant_service: TenantService = Depends(TenantService),
    db: AsyncSession = Depends(get_db),
    offset: int = 0,
    limit: int = 100,
    search: str | None = None,
    name: str | None = None,
    domain_name: str | None = None,
):
    try:
        tenants = await tenant_service.list_(
            db=db,
            offset=offset,
            limit=limit,
            search=search,
            name=name,
            domain_name=domain_name,
        )
        total = await tenant_service.count(
            db=db, search=search, name=name, domain_name=domain_name, filtered=False
        )
        filtered = await tenant_service.count(
            db=db, search=search, name=name, domain_name=domain_name, filtered=True
        )
        return {"items": tenants, "total": total, "filtered": filtered}
    except Exception as e:
        logger.exception("Failed to list tenants: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list tenants",
        )


@router.get(
    "/{tenant_uuid}",
    response_model=schemas.TenantResult,
    dependencies=[Depends(Permissions.TENANT_READ)],
)
async def get_tenant(
    tenant_uuid: str = Depends(valid_tenant_id),
    tenant_service: TenantService = Depends(TenantService),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves a tenant by UUID or slug."""
    return await tenant_service.get(tenant_uuid, db=db)


@router.put(
    "/{tenant_uuid}",
    response_model=schemas.TenantResult,
    dependencies=[Depends(Permissions.TENANT_UPDATE)],
)
async def update_tenant(
    tenant_uuid: str = Depends(valid_tenant_id),
    tenant_update: schemas.TenantUpdate = Depends(),
    tenant_service: TenantService = Depends(TenantService),
    db: AsyncSession = Depends(get_db),
):
    """Updates a tenant."""
    try:
        updated_tenant = await tenant_service.update(
            tenant_uuid, db=db, **tenant_update.model_dump()
        )
        return updated_tenant
    except Exception as e:
        logger.exception(f"Failed to update tenant {tenant_uuid}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update tenant"
        )


@router.delete(
    "/{tenant_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(Permissions.TENANT_DELETE)],
)
async def delete_tenant(
    tenant_uuid: str = Depends(valid_tenant_id),
    tenant_service: TenantService = Depends(TenantService),
    db: AsyncSession = Depends(get_db),
):
    """Deletes a tenant."""
    await tenant_service.delete(tenant_uuid, db=db)
    return  # 204 No Content


@router.get(
    "/{tenant_uuid}/domains",
    response_model=list[schemas.Domain],
    dependencies=[Depends(Permissions.TENANT_DOMAINS_READ)],
)
async def get_tenant_domains(
    tenant_uuid: str = Depends(valid_tenant_id),
    tenant_service: TenantService = Depends(TenantService),
    db: AsyncSession = Depends(get_db),
):
    """Lists all domains for a tenant."""
    return await tenant_service.list_domains(tenant_uuid, db=db)
