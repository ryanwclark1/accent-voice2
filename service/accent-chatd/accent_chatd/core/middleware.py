# src/accent_chatd/core/middleware.py
# Basic example of a middleware, which prints the request path.
from starlette.middleware.base import BaseHTTPMiddleware


class ExampleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(f"Request path: {request.url.path}")
        response = await call_next(request)
        return response
