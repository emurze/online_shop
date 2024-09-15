from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api_v1 import router as api_v1_router
from api_v1.auth.backend import fastapi_users, authentication_backend
from config import Config, configure_logging, app_config
from shared.db import get_db_adapter


def create_app(config: Config = app_config) -> FastAPI:
    db_adapter = get_db_adapter(config)

    @asynccontextmanager
    async def lifespan(app_: FastAPI) -> None:
        yield
        await db_adapter.dispose()

    configure_logging(config)
    app = FastAPI(
        title=config.api.title,
        docs_url=config.api.docs_url,
        redoc_url=config.api.redoc_url,
        lifespan=lifespan,
    )
    app.include_router(api_v1_router, prefix=config.api.v1_prefix)
    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=config.api.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
