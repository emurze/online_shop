from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api_v1 import router as api_v1_router
from config import AppConfig, configure_logging


def create_app(config: AppConfig = AppConfig()) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app_: FastAPI) -> None:
        yield

    configure_logging(config.log_level, config.debug)
    app = FastAPI(
        title=config.app_title,
        lifespan=lifespan,
    )
    app.include_router(api_v1_router, prefix=config.api_v1_prefix)
    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=config.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
