from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, cast

from dishka.integrations.fastapi import (
    setup_dishka as add_container_to_fastapi,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.application.common.application_error import ApplicationError
from auth.bootstrap.config import get_database_config, get_rabbitmq_config
from auth.bootstrap.container import bootstrap_api_container
from auth.infrastructure.persistence.sql_tables import (
    map_outbox_table,
    map_session_table,
    map_user_table,
)
from auth.presentation.api.exception_handlers import application_error_handler
from auth.presentation.api.middlewares.auth import (
    LoginMiddleware,
    LogoutMiddleware,
    RegistrationMiddleware,
)
from auth.presentation.api.routers.auth import AUTH_ROUTER
from auth.presentation.api.routers.healthcheck import HEALTHCHECK_ROUTER
from auth.presentation.api.routers.users import USERS_ROUTER

if TYPE_CHECKING:
    from dishka import AsyncContainer
    from starlette.types import HTTPExceptionHandler


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    map_outbox_table()
    map_user_table()
    map_session_table()

    dishka_container = cast("AsyncContainer", application.state.dishka_container)
    yield
    await dishka_container.close()


def add_middlewares(application: FastAPI) -> None:
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    application.add_middleware(RegistrationMiddleware)
    application.add_middleware(LoginMiddleware)
    application.add_middleware(LogoutMiddleware)


def add_api_routers(application: FastAPI) -> None:
    application.include_router(AUTH_ROUTER)
    application.include_router(USERS_ROUTER)
    application.include_router(HEALTHCHECK_ROUTER)


def add_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(
        ApplicationError,
        cast("HTTPExceptionHandler", application_error_handler),
    )


def bootstrap_application() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    dishka_container = bootstrap_api_container(
        get_rabbitmq_config(),
        get_database_config(),
    )

    add_middlewares(application)
    add_api_routers(application)
    add_exception_handlers(application)
    add_container_to_fastapi(dishka_container, application)

    return application
