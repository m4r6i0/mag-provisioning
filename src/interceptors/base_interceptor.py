from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response


class ExceptionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exception:
            return Response(
                content=str(http_exception.detail),
                status_code=http_exception.status_code,
            )
        except Exception as e:
            return Response(
                content=str(e),
                status_code=500,
            )