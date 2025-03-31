from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from auth.application.common.application_error import ApplicationError, ErrorType
from auth.application.common.markers.query import Query
from auth.application.models.user import UserReadModel
from auth.application.ports.identity_provider import IdentityProvider
from auth.application.ports.user_gateway import UserGateway


@dataclass(frozen=True)
class GetCurrentUser(Query[UserReadModel]): ...


class GetCurrentUserHandler(RequestHandler[GetCurrentUser, UserReadModel]):
    def __init__(
        self, user_gateway: UserGateway, identity_provider: IdentityProvider
    ) -> None:
        self._user_gateway = user_gateway
        self._identity_provider = identity_provider

    async def handle(self, request: GetCurrentUser) -> UserReadModel:
        user_id = self._identity_provider.current_user_id()
        user = await self._user_gateway.with_user_id(user_id)

        if user is None:
            raise ApplicationError(
                message="User not found", error_type=ErrorType.NOT_FOUND
            )

        return user
