from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from auth.application.common.markers.command import Command
from auth.domain.user.factory import UserFactory
from auth.domain.user.repository import UserRepository
from auth.domain.user.user_id import UserId


@dataclass(frozen=True)
class Registration(Command[UserId]):
    username: str
    password: str


class RegistrationHandler(RequestHandler[Registration, UserId]):
    def __init__(
        self,
        user_repository: UserRepository,
        user_factory: UserFactory,
    ) -> None:
        self._user_repository = user_repository
        self._user_factory = user_factory

    async def handle(self, request: Registration) -> UserId:
        user = await self._user_factory.create_user(
            username=request.username, password=request.password
        )

        self._user_repository.add(user)

        return user.entity_id
