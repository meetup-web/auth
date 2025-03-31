from abc import ABC, abstractmethod

from auth.application.models.session import SessionReadModel
from auth.domain.session.session_id import SessionId
from auth.domain.user.user_id import UserId


class SessionGateway(ABC):
    @abstractmethod
    async def with_user_id(self, user_id: UserId) -> list[SessionReadModel]: ...
    @abstractmethod
    async def with_session_id(self, session_id: SessionId) -> SessionReadModel | None: ...
