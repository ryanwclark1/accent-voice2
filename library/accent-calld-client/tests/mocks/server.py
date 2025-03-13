# tests/mock_server/server.py
from fastapi import FastAPI, HTTPException, Header, Depends, Body
from typing import Annotated, Any

app = FastAPI()


# Mock authentication
async def get_token_header(x_token: Annotated[str | None, Header()] = None):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="Invalid X-Token header")


# Mock data (using the same constants as conftest.py for consistency)
from ..conftest import (
    AGENT_ID,
    AGENT_NUMBER,
    EXTENSION,
    CONTEXT,
    LINE_ID,
    QUEUE_ID,
    TENANT_UUID,
    AGENT_STATUS_RESPONSE,
    AGENT_STATUSES_RESPONSE,
)
from accent_agentd_client.error import (  # Import error consts.
    ALREADY_IN_QUEUE,
    ALREADY_IN_USE,
    ALREADY_LOGGED,
    CONTEXT_DIFFERENT_TENANT,
    NOT_IN_QUEUE,
    NOT_LOGGED,
    NO_SUCH_AGENT,
    NO_SUCH_EXTEN,
    NO_SUCH_LINE,
    NO_SUCH_QUEUE,
    QUEUE_DIFFERENT_TENANT,
    UNAUTHORIZED,
)


# Helper function to simulate tenant checks (replace with your actual logic)
async def check_tenant(tenant_uuid: str | None = None):
    if tenant_uuid and tenant_uuid != TENANT_UUID:
        raise HTTPException(status_code=400, detail=CONTEXT_DIFFERENT_TENANT)


# --- Status Endpoint ---
@app.get("/api/agentd/1.0/status")
async def get_service_status():
    return {"status": "OK", "version": "1.0"}


# --- Agent Status Endpoints ---
@app.get("/api/agentd/1.0/by-id/{agent_id}", dependencies=[Depends(get_token_header)])
async def get_agent_status_by_id(
    agent_id: str, accent_tenant: Annotated[str | None, Header()] = None
):
    await check_tenant(accent_tenant)
    if agent_id == AGENT_ID:
        return AGENT_STATUS_RESPONSE
    raise HTTPException(status_code=404, detail=NO_SUCH_AGENT)


@app.get(
    "/api/agentd/1.0/by-number/{agent_number}", dependencies=[Depends(get_token_header)]
)
async def get_agent_status_by_number(
    agent_number: str, accent_tenant: Annotated[str | None, Header()] = None
):
    await check_tenant(accent_tenant)
    if agent_number == AGENT_NUMBER:
        return AGENT_STATUS_RESPONSE
    raise HTTPException(status_code=404, detail=NO_SUCH_AGENT)


@app.get("/api/agentd/1.0/users/me/agents", dependencies=[Depends(get_token_header)])
async def get_user_agent_status(accent_tenant: Annotated[str | None, Header()] = None):
    await check_tenant(accent_tenant)
    return AGENT_STATUS_RESPONSE  # Simplified user agent status


@app.get("/api/agentd/1.0", dependencies=[Depends(get_token_header)])
async def get_all_agent_statuses(
    recurse: bool = False, accent_tenant: Annotated[str | None, Header()] = None
):
    await check_tenant(accent_tenant)
    # In a real implementation, 'recurse' would affect the returned data.
    return AGENT_STATUSES_RESPONSE


# --- Queue Management Endpoints ---


@app.post(
    "/api/agentd/1.0/by-id/{agent_id}/add", dependencies=[Depends(get_token_header)]
)
async def add_agent_to_queue(
    agent_id: str,
    queue_data: dict[str, Any] = Body(...),
    accent_tenant: Annotated[str | None, Header()] = None,
):
    await check_tenant(accent_tenant)
    if agent_id != AGENT_ID:  # Simulate agent not found
        raise HTTPException(status_code=404, detail=NO_SUCH_AGENT)
    if queue_data.get("queue_id") != QUEUE_ID:  # Simulate queue not found
        raise HTTPException(status_code=404, detail=NO_SUCH_QUEUE)

    return  # Simulate success (204 No Content)


@app.post(
    "/api/agentd/1.0/by-id/{agent_id}/remove", dependencies=[Depends(get_token_header)]
)
async def remove_agent_from_queue(
    agent_id: str,
    queue_data: dict[str, Any] = Body(...),
    accent_tenant: Annotated[str | None, Header()] = None,
):
    await check_tenant(accent_tenant)
    if agent_id != AGENT_ID:
        raise HTTPException(status_code=404, detail=NO_SUCH_AGENT)
    if queue_data.get("queue_id") != QUEUE_ID:
        raise HTTPException(status_code=404, detail=NO_SUCH_QUEUE)

    return  # Simulate success (204 No Content)


# --- Agent Login/Logoff Endpoints ---


@app.post(
    "/api/agentd/1.0/by-id/{agent_id}/login", dependencies=[Depends(get_token_header)]
)
async def login_agent(
    agent_id: str,
    login_data: dict[str, Any] = Body(...),
    accent_tenant: Annotated[str | None, Header()] = None,
):
    await check_tenant(accent_tenant)
    if agent_id != AGENT_ID:
        raise HTTPException(status_code=404, detail=NO_SUCH_AGENT)
    if login_data.get("extension") != EXTENSION or login_data.get("context") != CONTEXT:
        raise HTTPException(status_code=404, detail=NO_SUCH_EXTEN)
    return


@app.post(
    "/api/agentd/1.0/by-number/{agent_number}/login",
    dependencies=[Depends(get_token_header)],
)
async def login_agent_by_number(
    agent_number: str,
    login_data: dict[str, Any] = Body(...),
    accent_tenant: Annotated[str | None, Header()] = None,
):
    await check_tenant(accent_tenant)
    if agent_number != AGENT_NUMBER:
        raise HTTPException(status_code=404, detail=NO_SUCH_AGENT)
    if login_data.get("extension") != EXTENSION or login_data.get("context") != CONTEXT:
        raise HTTPException(status_code=404, detail=NO_SUCH_EXTEN)

    return


@app.post(
    "/api/agentd/1.0/by-id/{agent_id}/logoff", dependencies=[Depends(get_token_header)]
)
async def logoff_agent(
    agent_id: str, accent_tenant: Annotated[str | None, Header()] = None
):
    await check_tenant(accent_tenant)
    if agent_id != AGENT_ID:
        raise HTTPException(status_code=404, detail=NO_SUCH_AGENT)
    return


@app.post(
    "/api/agentd/1.0/by-number/{agent_number}/logoff",
    dependencies=[Depends(get_token_header)],
)
async def logoff_agent_by_number(
    agent_number: str, accent_tenant: Annotated[str | None, Header()] = None
):
    await check_tenant(accent_tenant)
    if agent_number != AGENT_NUMBER:
        raise HTTPException(status_code=404, detail=NO_SUCH_AGENT)
    return


@app.post("/api/agentd/1.0/logoff", dependencies=[Depends(get_token_header)])
async def logoff_all_agents(
    recurse: bool = False, accent_tenant: Annotated[str | None, Header()] = None
):
    await check_tenant(accent_tenant)
    # 'recurse' would be used in a real implementation
    return


@app.post("/api/agentd/1.0/relog", dependencies=[Depends(get_token_header)])
async def relog_all_agents(
    recurse: bool = False, accent_tenant: Annotated[str | None, Header()] = None
):
    await check_tenant(accent_tenant)
    # 'recurse' would be used in a real implementation
    return


# --- User Agent Endpoints ---
@app.post(
    "/api/agentd/1.0/users/me/agents/login", dependencies=[Depends(get_token_header)]
)
async def login_user_agent(
    login_data: dict[str, Any] = Body(...),
    accent_tenant: Annotated[str | None, Header()] = None,
):
    await check_tenant(accent_tenant)
    if login_data.get("line_id") != LINE_ID:
        raise HTTPException(status_code=404, detail=NO_SUCH_LINE)
    return


@app.post(
    "/api/agentd/1.0/users/me/agents/logoff", dependencies=[Depends(get_token_header)]
)
async def logoff_user_agent(accent_tenant: Annotated[str | None, Header()] = None):
    await check_tenant(accent_tenant)
    return


@app.post(
    "/api/agentd/1.0/users/me/agents/pause", dependencies=[Depends(get_token_header)]
)
async def pause_user_agent(accent_tenant: Annotated[str | None, Header()] = None):
    await check_tenant(accent_tenant)
    return


@app.post(
    "/api/agentd/1.0/users/me/agents/unpause", dependencies=[Depends(get_token_header)]
)
async def unpause_user_agent(accent_tenant: Annotated[str | None, Header()] = None):
    await check_tenant(accent_tenant)
    return


# --- Agent Pause/Unpause by Number ---


@app.post(
    "/api/agentd/1.0/by-number/{agent_number}/pause",
    dependencies=[Depends(get_token_header)],
)
async def pause_agent_by_number(
    agent_number: str, accent_tenant: Annotated[str | None, Header()] = None
):
    await check_tenant(accent_tenant)
    if agent_number != AGENT_NUMBER:
        raise HTTPException(status_code=404, detail=NO_SUCH_AGENT)
    return


@app.post(
    "/api/agentd/1.0/by-number/{agent_number}/unpause",
    dependencies=[Depends(get_token_header)],
)
async def unpause_agent_by_number(
    agent_number: str, accent_tenant: Annotated[str | None, Header()] = None
):
    await check_tenant(accent_tenant)
    if agent_number != AGENT_NUMBER:
        raise HTTPException(status_code=404, detail=NO_SUCH_AGENT)
    return
