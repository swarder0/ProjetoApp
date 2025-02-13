from fastapi import FastAPI

from src.application.v1.router import router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Estudo",
        description="Estudo de FastAPI",
        docs_url="/estudo/api/docs",
        openapi_url="/estudo/api/openapi.json"
)

    app.include_router(router=router, prefix="/estudo/api")
    return app

app = create_app()