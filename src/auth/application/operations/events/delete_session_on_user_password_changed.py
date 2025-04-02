from bazario.asyncio import NotificationHandler

from auth.application.ports.identity_provider import IdentityProvider
from auth.domain.session.repository import SessionRepository
from auth.domain.user.events import UserPasswordChanged


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
