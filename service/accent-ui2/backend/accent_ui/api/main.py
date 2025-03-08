from fastapi import APIRouter

# from accent_ui.api.routes import items, login, private, users, utils
from accent_ui.core.config import settings

api_router = APIRouter()
# api_router.include_router(login.router)
# api_router.include_router(users.router)
# api_router.include_router(utils.router)
# api_router.include_router(items.router)


if settings.ENVIRONMENT == "local":
  print("Local environment detected. Including private routes.")
    # api_router.include_router(private.router)
