from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from auth.application.common.application_error import ApplicationError, ErrorType
from auth.application.common.markers.query import Query
from auth.application.models.session import SessionReadModel
from auth.application.ports.identity_provider import IdentityProvider
from auth.application.ports.session_gateway import SessionGateway


@dataclass(frozen=True)
class GetCurrentSession(Query[SessionReadModel]): ...


class GetCurrentSessionHandler(RequestHandler[GetCurrentSession, SessionReadModel]):
    def __init__(
        self, identity_provider: IdentityProvider, session_gateway: SessionGateway
    ) -> None:
        self._identity_provider = identity_provider
        self._session_gateway = session_gateway

    async def handle(self, request: GetCurrentSession) -> SessionReadModel:
        session_id = self._identity_provider.current_session_id()

        session = await self._session_gateway.with_session_id(session_id)

        if not session:
            raise ApplicationError(
                message="Invalid session", error_type=ErrorType.AUTHORIZATION_ERROR
            )

        return session
