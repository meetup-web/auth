from typing import TYPE_CHECKING, Final, cast

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from auth.application.ports.session_registry import SessionRegistry

if TYPE_CHECKING:
    from dishka import AsyncContainer


class LoginMiddleware(BaseHTTPMiddleware):
    _SESSION_COOKIE_NAME: Final[str] = "session_id"
    _REQUEST_PATH: Final[str] = "/auth/sign-in"

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        if not request.url.path.startswith(self._REQUEST_PATH):
            return response

        dishka_container = cast("AsyncContainer", request.state.dishka_container)

        async with dishka_container() as container:
            session_registry = await container.get(SessionRegistry)

        session = session_registry.raise_session()

        if not session:
            return response

        response.set_cookie(
            key=self._SESSION_COOKIE_NAME,
            value=str(session.session_id),
            expires=session.expires_at,
        )

        return response


class RegistrationMiddleware(BaseHTTPMiddleware):
    _SESSION_COOKIE_NAME: Final[str] = "session_id"
    _REQUEST_PATH: Final[str] = "/auth/sign-up"

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        if not request.url.path.startswith(self._REQUEST_PATH):
            return response

        dishka_container = cast("AsyncContainer", request.state.dishka_container)

        async with dishka_container() as container:
            session_registry = await container.get(SessionRegistry)

        session = session_registry.raise_session()

        if not session:
            return response

        response.set_cookie(
            key=self._SESSION_COOKIE_NAME,
            value=str(session.session_id),
            expires=session.expires_at,
        )

        return response


class LogoutMiddleware(BaseHTTPMiddleware):
    _SESSION_COOKIE_NAME: Final[str] = "session_id"
    _REQUEST_PATH: Final[str] = "/auth/sign-out"

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        if not request.url.path.startswith(self._REQUEST_PATH):
            return response

        response.delete_cookie(self._SESSION_COOKIE_NAME)

        return response
