from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from auth.application.common.application_error import ApplicationError, ErrorType
from auth.application.common.markers.command import Command
from auth.application.ports.identity_provider import IdentityProvider
from auth.application.ports.password_checker import PasswordChecker
from auth.application.ports.time_provider import TimeProvider
from auth.domain.user.events import UserDeleted
from auth.domain.user.repository import UserRepository


@dataclass(frozen=True)
class DeleteUser(Command[None]):
    password: str


class DeleteUserHandler(RequestHandler[DeleteUser, None]):
    def __init__(
        self,
        user_repository: UserRepository,
        identity_provider: IdentityProvider,
        password_checker: PasswordChecker,
        time_provider: TimeProvider,
    ) -> None:
        self._user_repository = user_repository
        self._identity_provider = identity_provider
        self._password_checker = password_checker
        self._time_provider = time_provider

    async def handle(self, request: DeleteUser) -> None:
        user_id = self._identity_provider.current_user_id()
        user = await self._user_repository.with_id(user_id)

        if user is None:
            raise ApplicationError(
                message="User not found", error_type=ErrorType.NOT_FOUND
            )

        if not self._password_checker.check_password(
            password=request.password, hashed_password=user.password
        ):
            raise ApplicationError(
                message="Invalid password", error_type=ErrorType.VALIDATION_ERROR
            )

        await self._user_repository.delete(user)

        event = UserDeleted(
            user_id=user_id, event_date=self._time_provider.provide_current()
        )

        user.add_event(event=event)
        await self._user_repository.delete(user)
