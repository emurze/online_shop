from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import AppConfig

def create_app(config: AppConfig = AppConfig()) -> FastAPI:
    app = FastAPI(title=config.app_title)
    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=config.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app