from fastapi import FastAPI

from app.core.http_errors import HttpErrors
from app.routers import file_search_poc
from app.routers.auth import auth_v1
from app.routers.blocks import blocks_v1
from app.routers.districts import districts_v1
from app.core.api_checks_mw import ApiChecksMW
from app.core.core_exceptions import UnauthorizedException, InvalidRequestException, \
    NotFoundException, ConflictException, NotAcceptable



# todo check whether we need API Support
# api_key_header = APIKeyHeader()


# todo check auth
# oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


def create_app() -> FastAPI:
    '''
        For creating and configuring the FastAPI application
    '''

    app = FastAPI(
        title="GramSevak Seva",
        description="APIs for management",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # app.include_router(file_search_poc.router)
    app.include_router(auth_v1.router)
    app.include_router(blocks_v1.router)
    app.include_router(districts_v1.router)

    app.add_middleware(ApiChecksMW)

    # Adding Exceptions:

    @app.exception_handler(InvalidRequestException)
    async def invalid_exception_handler(e: InvalidRequestException):
        return await HttpErrors.http_400(e)

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_exception_handler(e: UnauthorizedException):
        return await HttpErrors.http_401(e)

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(e: NotFoundException):
        return await HttpErrors.http_404(e)

    @app.exception_handler(NotAcceptable)
    async def not_acceptable_exception_handler(e: NotAcceptable):
        return await HttpErrors.http_406(e)

    @app.exception_handler(ConflictException)
    async def conflict_exception_handler(e: ConflictException):
        return await HttpErrors.http_409(e)

    return app
