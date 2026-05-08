"""FastAPI application entrypoint."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings
from .data_loader import get_knowledge_data
from .routers import (
    ask,
    change_safety,
    flows,
    glossary,
    health,
    knowledge_health,
    onboarding,
    services,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_knowledge_data()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Payments Platform Navigator API",
        description="Deterministic API over synthetic payments platform knowledge.",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        if isinstance(exc.detail, dict) and "code" in exc.detail:
            payload = {"error": exc.detail}
        else:
            payload = {
                "error": {
                    "code": "http_error",
                    "message": str(exc.detail),
                    "details": {},
                }
            }
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "validation_error",
                    "message": "Request validation failed.",
                    "details": {"errors": exc.errors()},
                }
            },
        )

    app.include_router(health.router)
    app.include_router(services.router)
    app.include_router(flows.router)
    app.include_router(glossary.router)
    app.include_router(onboarding.router)
    app.include_router(knowledge_health.router)
    app.include_router(ask.router)
    app.include_router(change_safety.router)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=False)
