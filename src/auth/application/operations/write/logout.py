from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from auth.application.common.application_error import ApplicationError, ErrorType
from auth.application.common.markers.command import Command
from auth.application.ports.identity_provider import IdentityProvider
from auth.domain.session.repository import SessionRepository


@dataclass(frozen=True)
class Logout(Command[None]): ...


class LogoutHandler(RequestHandler[Logout, None]):
    def __init__(
        self,
        session_repository: SessionRepository,
        identity_provider: IdentityProvider,
    ) -> None:
        self._session_repository = session_repository
        self._identity_provider = identity_provider

    async def handle(self, request: Logout) -> None:
        session_id = self._identity_provider.current_session_id()

        session = await self._session_repository.with_id(session_id)

        if not session:
            raise ApplicationError(
                message="Invalid session", error_type=ErrorType.AUTHORIZATION_ERROR
            )

        await self._session_repository.delete(session)
