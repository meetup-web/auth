from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from auth.application.common.markers.query import Query
from auth.application.models.session import SessionReadModel
from auth.application.ports.identity_provider import IdentityProvider
from auth.application.ports.session_gateway import SessionGateway


@dataclass(frozen=True)
class GetUserSessions(Query[list[SessionReadModel]]): ...


class GetUserSessionsHandler(RequestHandler[GetUserSessions, list[SessionReadModel]]):
    def __init__(
        self, identity_provider: IdentityProvider, session_gateway: SessionGateway
    ) -> None:
        self._identity_provider = identity_provider
        self._session_gateway = session_gateway

    async def handle(self, request: GetUserSessions) -> list[SessionReadModel]:
        user_id = self._identity_provider.current_user_id()
        sessions = await self._session_gateway.with_user_id(user_id)
        return sessions
