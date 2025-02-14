from fastapi import FastAPI
from app.routers import file_search_poc
from app.routers.auth import auth_v1
from app.core.api_checks_mw import ApiChecksMW


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

    app.add_middleware(ApiChecksMW)

    return app
