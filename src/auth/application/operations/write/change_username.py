from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from auth.application.common.application_error import ApplicationError, ErrorType
from auth.application.common.markers.command import Command
from auth.application.ports.identity_provider import IdentityProvider
from auth.application.ports.time_provider import TimeProvider
from auth.domain.user.repository import UserRepository


@dataclass(frozen=True)
class ChangeUsername(Command[None]):
    new_username: str


class ChangeUsernameHandler(RequestHandler[ChangeUsername, None]):
    def __init__(
        self,
        user_repository: UserRepository,
        identity_provider: IdentityProvider,
        time_provider: TimeProvider,
    ) -> None:
        self._user_repository = user_repository
        self._identity_provider = identity_provider
        self._time_provider = time_provider

    async def handle(self, request: ChangeUsername) -> None:
        user_id = self._identity_provider.current_user_id()
        user = await self._user_repository.with_id(user_id)

        if user is None:
            raise ApplicationError(
                message="User not found", error_type=ErrorType.NOT_FOUND
            )

        user.change_username(
            username=request.new_username,
            current_date=self._time_provider.provide_current(),
        )
