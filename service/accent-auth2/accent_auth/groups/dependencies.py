# accent_auth/groups/dependencies.py
from typing import Annotated

from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from accent_auth.db import DAO
from accent_auth.db.engine import AsyncSessionLocal

# from accent_auth.utils.helpers import is_uuid  # Moved
from accent_auth.utils import is_uuid
from contextlib import asynccontextmanager
from accent_auth.users.dependencies import valid_user_id, valid_token
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
