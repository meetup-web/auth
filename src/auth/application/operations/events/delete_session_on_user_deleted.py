from bazario.asyncio import NotificationHandler

from auth.domain.session.repository import SessionRepository
from auth.domain.user.events import UserDeleted


class DeleteSessionsOnUserDeletedHandler(NotificationHandler[UserDeleted]):
    def __init__(self, session_repository: SessionRepository) -> None:
        self._session_repository = session_repository

    async def handle(self, notification: UserDeleted) -> None:
        sessions = await self._session_repository.with_user_id(notification.user_id)

        for session in sessions:
            await self._session_repository.delete(session)
