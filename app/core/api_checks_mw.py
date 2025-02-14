from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from fastapi import Request


class ApiChecksMW(BaseHTTPMiddleware):

    def __int__(self, app: ASGIApp):
        super().__init__(app)

    @staticmethod
    async def __read_jwt(request: Request):
        """
            Reading and verifying the JWT token from request header
            Returns user_id from the decoded token
        """

        try:
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer"):
                raise ValueError("Invalid Auth Header")

        except ValueError as e:
            raise



        pass

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
            This is an overridden method to define a custom logic to process incoming requests.
            i.e Middleware
        """
        method = request.method
        path = request.url.path



        pass