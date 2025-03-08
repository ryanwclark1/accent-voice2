# accent_auth/users/dependencies.py
from typing import Annotated

from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from accent_auth.db import DAO
from accent_auth.db.engine import AsyncSessionLocal
from accent_auth.utils.helpers import is_uuid
from contextlib import asynccontextmanager


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


async def valid_user_id(
    user_uuid: str,
    dao: DAO = Depends(DAO.from_defaults),
    db: AsyncSession = Depends(get_db),
) -> str:
    if not is_uuid(user_uuid):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_uuid format"
        )

    if not await dao.user.exists(user_uuid, session=db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user_uuid


async def valid_email_id(
    email_uuid: str,
    dao: DAO = Depends(DAO.from_defaults),
    db: AsyncSession = Depends(get_db),
) -> str:
    if not is_uuid(email_uuid):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email_uuid format"
        )
    try:
        await dao.email.get(email_uuid, session=db)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email not found"
        )
    return email_uuid


async def valid_session_id(
    session_uuid: str,
    dao: DAO = Depends(DAO.from_defaults),
    db: AsyncSession = Depends(get_db),
) -> str:
    if not is_uuid(session_uuid):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid session_uuid format",
        )

    if not await dao.session.get(session_uuid, session=db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    return session_uuid


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
    USER_CREATE = Depends(get_db)  # Example: Any valid DB connection = can create.
    USER_READ = Depends(valid_user_id)  # Requires a valid user ID.
    USER_UPDATE = Depends(valid_user_id)  # Requires a valid user ID.
    USER_DELETE = Depends(valid_user_id)  # Requires a valid user ID.
    USER_EMAIL_CONFIRM = Depends(valid_user_id)
    USER_SESSION_READ = Depends(valid_user_id)
    USER_SESSION_DELETE = (
        Depends(valid_user_id),
        Depends(valid_session_id),
    )  # Requires both user and session.
    USER_PW_UPDATE = Depends(valid_user_id)
