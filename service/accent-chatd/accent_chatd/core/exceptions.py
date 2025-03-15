# src/accent_chatd/core/exceptions.py
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom exception handler for HTTP exceptions.
    Formats the response to be consistent with the original Flask API.
    """
    # Construct a dictionary in the same format as the original Flask API
    error_response = {
        "message": exc.detail,
        "error_id": getattr(exc, "id_", "unknown-error"),  # Fallback to "unknown-error"
        "details": getattr(exc, "details", {}),  # Fallback to empty dict
        "timestamp": int(datetime.datetime.now().timestamp()),  # posix timestamp
    }

    resource = getattr(exc, "resource", None)
    if resource:
        error_response["resource"] = resource

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response,
    )
