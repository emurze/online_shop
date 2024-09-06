from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import AppConfig
from pizzas.api import router as pizzas_router


def create_app(config: AppConfig = AppConfig()) -> FastAPI:
    app = FastAPI(title=config.app_title)
    app.include_router(pizzas_router)
    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=config.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
