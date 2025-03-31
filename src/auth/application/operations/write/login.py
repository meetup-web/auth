from dataclasses import dataclass

from bazario.asyncio import Publisher, RequestHandler
from bazario.markers import Notification

from auth.application.common.application_error import ApplicationError, ErrorType
from auth.application.common.markers.command import Command
from auth.application.ports.password_checker import PasswordChecker
from auth.domain.user.repository import UserRepository
from auth.domain.user.user_id import UserId


@dataclass(frozen=True)
class Login(Command[UserId]):
    username: str
    password: str


@dataclass(frozen=True)
class UserLoggedIn(Notification):
    user_id: UserId


class LoginHandler(RequestHandler[Login, UserId]):
    def __init__(
        self,
        user_repository: UserRepository,
        password_checker: PasswordChecker,
        notification_publisher: Publisher,
    ) -> None:
        self._user_repository = user_repository
        self._password_checker = password_checker
        self._notification_publisher = notification_publisher

    async def handle(self, request: Login) -> UserId:
        user = await self._user_repository.with_username(username=request.username)

        if not user:
            raise ApplicationError(
                error_type=ErrorType.AUTHORIZATION_ERROR,
                message="Invalid username or password",
            )

        if not self._password_checker.check_password(
            password=request.password, hashed_password=user.password
        ):
            raise ApplicationError(
                error_type=ErrorType.AUTHORIZATION_ERROR,
                message="Invalid username or password",
            )

        await self._notification_publisher.publish(UserLoggedIn(user_id=user.entity_id))

        return user.entity_id
