from fastapi import APIRouter, Depends
from accent_ui.helpers.service import get_confd_service

router = APIRouter()

@router.get("/")
async def list_resources(
    limit: int = 10, offset: int = 0, service=Depends(get_confd_service)
):
    """List resources with pagination."""
    return service.list(limit=limit, offset=offset)

@router.post("/")
async def create_resource(
    resource: dict, service=Depends(get_confd_service)
):
    """Create a new resource."""
    return service.create(resource)

@router.get("/{resource_id}")
async def get_resource(
    resource_id: str, service=Depends(get_confd_service)
):
    """Get a specific resource by ID."""
    return service.get(resource_id)

@router.put("/{resource_id}")
async def update_resource(
    resource_id: str, resource: dict, service=Depends(get_confd_service)
):
    """Update a resource by ID."""
    resource["id"] = resource_id
    service.update(resource)
    return {"status": "updated"}

@router.delete("/{resource_id}")
async def delete_resource(
    resource_id: str, service=Depends(get_confd_service)
):
    """Delete a resource by ID."""
    service.delete(resource_id)
    return {"status": "deleted"}
