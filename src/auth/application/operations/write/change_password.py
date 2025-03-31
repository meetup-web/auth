from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from auth.application.common.application_error import ApplicationError, ErrorType
from auth.application.common.markers.command import Command
from auth.application.ports.identity_provider import IdentityProvider
from auth.application.ports.password_checker import PasswordChecker
from auth.application.ports.password_hasher import PasswordHasher
from auth.application.ports.time_provider import TimeProvider
from auth.domain.user.repository import UserRepository


@dataclass(frozen=True)
class ChangePassword(Command[None]):
    current_password: str
    new_password: str


class ChangePasswordHandler(RequestHandler[ChangePassword, None]):
    def __init__(
        self,
        identity_provider: IdentityProvider,
        time_provider: TimeProvider,
        password_hasher: PasswordHasher,
        password_checker: PasswordChecker,
        user_repository: UserRepository,
    ) -> None:
        self._identity_provider = identity_provider
        self._time_provider = time_provider
        self._password_hasher = password_hasher
        self._password_checker = password_checker
        self._user_repository = user_repository

    async def handle(self, request: ChangePassword) -> None:
        user_id = self._identity_provider.current_user_id()
        user = await self._user_repository.with_id(user_id)

        if not user:
            raise ApplicationError(
                message="User not found", error_type=ErrorType.NOT_FOUND
            )

        if not self._password_checker.check_password(
            password=request.current_password, hashed_password=user.password
        ):
            raise ApplicationError(
                message="Invalid password", error_type=ErrorType.AUTHORIZATION_ERROR
            )

        user.change_password(
            password=self._password_hasher.hash_password(request.new_password),
            current_date=self._time_provider.provide_current(),
        )
