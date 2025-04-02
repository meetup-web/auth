from auth.application.common.application_error import ApplicationError, ErrorType
from auth.application.ports.id_generator import IdGenerator
from auth.application.ports.password_hasher import PasswordHasher
from auth.application.ports.time_provider import TimeProvider
from auth.domain.shared.events import DomainEventAdder
from auth.domain.user.events import UserCreated
from auth.domain.user.factory import UserFactory
from auth.domain.user.repository import UserRepository
from auth.domain.user.user import User


class UserFactoryImpl(UserFactory):
    def __init__(
        self,
        password_hasher: PasswordHasher,
        time_provider: TimeProvider,
        id_generator: IdGenerator,
        event_adder: DomainEventAdder,
        user_repository: UserRepository,
    ) -> None:
        self._password_hasher = password_hasher
        self._time_provider = time_provider
        self._id_generator = id_generator
        self._event_adder = event_adder
        self._user_repository = user_repository

    async def create_user(self, username: str, password: str) -> User:
        if await self._user_repository.with_username(username):
            raise ApplicationError(
                message="User already exists", error_type=ErrorType.ALREADY_EXISTS
            )

        user = User(
            entity_id=self._id_generator.generate_user_id(),
            event_adder=self._event_adder,
            password=self._password_hasher.hash_password(password),
            username=username,
            created_at=self._time_provider.provide_current(),
        )
        event = UserCreated(
            user_id=user.entity_id,
            username=user.username,
            password=user.password,
            event_date=user.created_at,
        )
        user.add_event(event)

        return user
