from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from accent_ui.helpers.service import get_confd_service

templates = Jinja2Templates(directory="accent_ui/templates")
router = APIRouter()

@router.get("/resources", response_class=HTMLResponse)
async def list_resources(request: Request, service=Depends(get_confd_service)):
    resources = service.list()
    return templates.TemplateResponse("resources/list.html", {"request": request, "resources": resources})

@router.get("/resources/{resource_id}", response_class=HTMLResponse)
async def resource_detail(request: Request, resource_id: str, service=Depends(get_confd_service)):
    resource = service.get(resource_id)
    return templates.TemplateResponse("resources/detail.html", {"request": request, "resource": resource})
