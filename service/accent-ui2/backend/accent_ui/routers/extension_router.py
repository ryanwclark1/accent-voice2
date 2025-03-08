from fastapi import APIRouter, Depends
from accent_ui.helpers.extension import get_extension_service

router = APIRouter()

@router.get("/")
async def list_extensions(
    limit: int = 10, offset: int = 0, service=Depends(get_extension_service)
):
    """List extensions with pagination."""
    return service.list(limit=limit, offset=offset)

@router.post("/")
async def create_extension(
    resource: dict, service=Depends(get_extension_service)
):
    """Create a new extension."""
    return service.create(resource)

@router.get("/{resource_id}")
async def get_extension(
    resource_id: str, service=Depends(get_extension_service)
):
    """Get a specific extension by ID."""
    return service.get(resource_id)

@router.put("/{resource_id}")
async def update_extension(
    resource_id: str, resource: dict, service=Depends(get_extension_service)
):
    """Update an extension by ID."""
    resource["id"] = resource_id
    service.update(resource)
    return {"status": "updated"}

@router.delete("/{resource_id}")
async def delete_extension(
    resource_id: str, service=Depends(get_extension_service)
):
    """Delete an extension by ID."""
    service.delete(resource_id)
    return {"status": "deleted"}
