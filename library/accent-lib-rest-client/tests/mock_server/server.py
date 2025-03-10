# Copyright 2025 Accent Communications

"""Mock server for testing accent-lib-rest-client."""

from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Create FastAPI app
security = HTTPBasic()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application for testing."""
    app = FastAPI(title="Accent REST Client Test Server")

    # Authentication middleware
    def verify_credentials(
        credentials: HTTPBasicCredentials = Depends(security),
    ) -> str:
        correct_username = "testuser"
        correct_password = "testpass"
        if (
            credentials.username != correct_username
            or credentials.password != correct_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        return credentials.username

    # Routes
    @app.get("/v1/test")
    async def test_endpoint() -> JSONResponse:
        """Basic test endpoint."""
        return JSONResponse(content={"message": "Test endpoint"})

    @app.get("/v1/test/data")
    async def get_data() -> dict[str, Any]:
        """Return test data."""
        return {
            "data": "test value",
            "status": "success",
            "timestamp": datetime.now().isoformat(),
        }

    @app.post("/v1/test/create")
    async def create_item(item: dict[str, Any]) -> dict[str, Any]:
        """Create a new item."""
        return {
            "id": "new-item",
            "status": "created",
            "data": item,
            "timestamp": datetime.now().isoformat(),
        }

    @app.get("/v1/error")
    async def server_error() -> JSONResponse:
        """Return a server error."""
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Server error occurred"},
        )

    @app.get("/v1/not-found")
    async def not_found() -> JSONResponse:
        """Return a not found error."""
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Resource not found"},
        )

    @app.get("/v1/auth")
    async def auth_endpoint(
        username: str = Depends(verify_credentials),
    ) -> dict[str, Any]:
        """Endpoint that requires authentication."""
        return {
            "message": f"Hello, {username}!",
            "authenticated": True,
            "expires": (datetime.now() + timedelta(hours=1)).isoformat(),
        }

    @app.get("/v1/echo-headers")
    async def echo_headers(request: Any) -> dict[str, Any]:
        """Echo the request headers."""
        return {"headers": dict(request.headers)}

    @app.get("/v1/tenant/{tenant_id}")
    async def tenant_endpoint(tenant_id: str) -> dict[str, Any]:
        """Endpoint that works with tenant information."""
        return {
            "tenant_id": tenant_id,
            "name": f"Tenant {tenant_id}",
            "status": "active",
        }

    return app


if __name__ == "__main__":
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8000)
