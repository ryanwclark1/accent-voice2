from fastapi import APIRouter

from .extension_router import router as extension_router
from .jinja_router import router as jinja_router
from .resource_router import router as resource_router

# REST API Router
api_router = APIRouter()
api_router.include_router(resource_router, prefix="/resources", tags=["Resources"])
api_router.include_router(extension_router, prefix="/extensions", tags=["Extensions"])

# Jinja2 Router
jinja_router = APIRouter()
jinja_router.include_router(jinja_router, prefix="/pages", tags=["Pages"])
