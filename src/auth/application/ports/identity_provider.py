from abc import ABC, abstractmethod

from auth.domain.session.session_id import SessionId
from auth.domain.user.user_id import UserId


class IdentityProvider(ABC):
    @abstractmethod
    def current_user_id(self) -> UserId: ...
    @abstractmethod
    def current_session_id(self) -> SessionId: ...
