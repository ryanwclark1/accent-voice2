# accent_auth/auth/dependencies.py

from typing import Annotated

from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from accent_auth.db import DAO
from accent_auth.db.engine import AsyncSessionLocal
from accent_auth.utils.helpers import is_uuid
# from contextlib import asynccontextmanager # Removed, not necessary

# async def get_db() -> AsyncSession:  # This is now in main dependencies file
#     """Dependency that provides a new async database session per request."""
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#             await session.commit()
#         except Exception:
#             await session.rollback()
#             raise
#         finally:
#             await session.close()


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
    CONFIG_READ = Depends(get_db)
    CONFIG_UPDATE = Depends(get_db)
