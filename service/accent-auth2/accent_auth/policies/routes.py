# accent_auth/policies/routes.py

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# from accent_auth.db.engine import AsyncSessionLocal  # REMOVED
from accent_auth.services.policy import PolicyService
from accent_auth.dependencies import get_db
from accent_auth.policies.dependencies import (
    valid_policy_id,
    Permissions,
)  # Import Permissions
from .schemas import PolicyCreate, PolicyUpdate, Policy, PolicyList, Access
from accent_auth import exceptions

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/policies",
    tags=["policies"],
)

@router.post("/", response_model=Policy, status_code=status.HTTP_201_CREATED, dependencies=[Depends(Permissions.POLICY_CREATE)])
async def create_policy(
    policy: PolicyCreate,
    policy_service: PolicyService = Depends(PolicyService),
    db: AsyncSession = Depends(get_db),
):
    """Creates a new policy."""
    try:
        return await policy_service.create(db=db, **policy.model_dump())
    except exceptions.DuplicatePolicyException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.exception("Failed to create policy: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/", response_model=PolicyList, dependencies=[Depends(Permissions.POLICY_READ)])
async def list_policies(
    policy_service: PolicyService = Depends(PolicyService),
    db: AsyncSession = Depends(get_db),
    offset: int = 0,
    limit: int = 100,
    search: str | None = None,
    name: str | None = None,
    slug: str | None = None,
    user_uuid: str | None = None,
    group_uuid: str | None = None,
    tenant_uuid: str | None = None,
    read_only: bool | None = None,
    shared:  bool | None = None
):
    """Lists policies with pagination."""
    try:
        policies = await policy_service.list_(db=db, offset=offset, limit=limit, search=search, name=name, slug=slug, user_uuid=user_uuid, group_uuid=group_uuid, tenant_uuid=tenant_uuid, read_only=read_only, shared=shared)
        total = await policy_service.count(db=db, search=search, name=name, slug=slug, user_uuid=user_uuid, group_uuid=group_uuid, tenant_uuid=tenant_uuid, read_only=read_only, shared=shared,filtered=False)
        filtered = await policy_service.count(db=db, search=search, name=name, slug=slug, user_uuid=user_uuid, group_uuid=group_uuid, tenant_uuid=tenant_uuid, read_only=read_only, shared=shared,filtered=True)
        return {"items": policies, "total": total, "filtered": filtered}
    except Exception as e:
        logger.exception("Failed to list policies: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

@router.get("/{policy_uuid}", response_model=Policy, dependencies=[Depends(Permissions.POLICY_READ)])
async def get_policy(
    policy_uuid: str = Depends(valid_policy_id),
    policy_service: PolicyService = Depends(PolicyService),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves a policy by UUID or slug."""
    policy = await policy_service.get(policy_uuid, db=db)  # No need to check None
    return policy

@router.put("/{policy_uuid}", response_model=Policy, dependencies=[Depends(Permissions.POLICY_UPDATE)])
async def update_policy(
    policy_uuid: str = Depends(valid_policy_id),
    policy_update: PolicyUpdate,
    policy_service: PolicyService = Depends(PolicyService),
    db: AsyncSession = Depends(get_db),
):
    """Updates a policy."""
    try:
        updated_policy = await policy_service.update(
            policy_uuid, db=db, **policy_update.model_dump()
        )
        return updated_policy
    except exceptions.DuplicatePolicyException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.exception(f"Failed to update policy {policy_uuid}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update policy"
        )


@router.delete("/{policy_uuid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(Permissions.POLICY_DELETE)])
async def delete_policy(
    policy_uuid: str = Depends(valid_policy_id),
    policy_service: PolicyService = Depends(PolicyService),
    db: AsyncSession = Depends(get_db),
):
    """Deletes a policy."""
    await policy_service.delete(policy_uuid, db=db)
    return  # 204 No Content


@router.put(
    "/{policy_uuid}/acl/{access}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(Permissions.POLICY_UPDATE)]
)
async def add_policy_access(
    policy_uuid: str = Depends(valid_policy_id),
    access: str,
    policy_service: PolicyService = Depends(PolicyService),
    db: AsyncSession = Depends(get_db),
):

    """Adds an access to a policy."""
    await policy_service.add_access(policy_uuid, access, db=db)
    return


@router.delete(
    "/{policy_uuid}/acl/{access}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(Permissions.POLICY_UPDATE)]
)
async def remove_policy_access(
    policy_uuid: str = Depends(valid_policy_id),
    access: str,
    policy_service: PolicyService = Depends(PolicyService),
    db: AsyncSession = Depends(get_db),
):
    """Removes an access from a policy."""
    await policy_service.delete_access(policy_uuid, access, db=db)
    return