from bazario.asyncio import NotificationHandler

from auth.application.models.session import SessionReadModel
from auth.application.ports.session_registry import SessionRegistry
from auth.domain.session.factory import SessionFactory
from auth.domain.session.repository import SessionRepository
from auth.domain.user.events import UserCreated


class CreateSessionOnUserCreatedHandler(NotificationHandler[UserCreated]):
    def __init__(
        self,
        session_factory: SessionFactory,
        session_repository: SessionRepository,
        session_registry: SessionRegistry,
    ) -> None:
        self._session_factory = session_factory
        self._session_repository = session_repository
        self._session_registry = session_registry

    async def handle(self, notification: UserCreated) -> None:
        session = self._session_factory.create_session(user_id=notification.user_id)

        self._session_repository.add(session)
        self._session_registry.set_session(
            SessionReadModel(session.entity_id, session.user_id, session.expires_at)
        )
