from typing import Final
from uuid import UUID

from fastapi import Request

from auth.application.common.application_error import ApplicationError, ErrorType
from auth.application.ports.identity_provider import IdentityProvider
from auth.domain.session.session_id import SessionId
from auth.domain.user.user_id import UserId


class HttpIdentityProvider(IdentityProvider):
    _USER_ID_HEADER: Final[str] = "X-User-Id"
    _SESSION_COOKIE_NAME: Final[str] = "session_id"

    def __init__(self, request: Request) -> None:
        self._request = request

    def current_user_id(self) -> UserId:
        user_id = self._request.headers.get(self._USER_ID_HEADER)

        if not user_id:
            raise ApplicationError(
                message="User not provided", error_type=ErrorType.AUTHORIZATION_ERROR
            )

        return UserId(UUID(user_id))

    def current_session_id(self) -> SessionId:
        session_id = self._request.cookies.get(self._SESSION_COOKIE_NAME)

        if not session_id:
            raise ApplicationError(
                message="Session not provided", error_type=ErrorType.AUTHORIZATION_ERROR
            )

        return SessionId(UUID(session_id))
