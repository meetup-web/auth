from bazario.asyncio import NotificationHandler

from auth.application.ports.identity_provider import IdentityProvider
from auth.domain.session.repository import SessionRepository
from auth.domain.user.events import UserDeleted, UserPasswordChanged


class DeleteSessionsOnUserDeletedHandler(NotificationHandler[UserDeleted]):
    def __init__(self, session_repository: SessionRepository) -> None:
        self._session_repository = session_repository

    async def handle(self, notification: UserDeleted) -> None:
        sessions = await self._session_repository.with_user_id(notification.user_id)

        for session in sessions:
            await self._session_repository.delete(session)


class DeleteSessionsOnUserPasswordChangedHandler(
    NotificationHandler[UserPasswordChanged]
):
    def __init__(
        self, session_repository: SessionRepository, identity_provider: IdentityProvider
    ) -> None:
        self._session_repository = session_repository
        self._identity_provider = identity_provider

    async def handle(self, notification: UserPasswordChanged) -> None:
        current_session_id = self._identity_provider.current_session_id()
        sessions = await self._session_repository.with_user_id(notification.user_id)

        for session in sessions:
            if session.entity_id != current_session_id:
                await self._session_repository.delete(session)
