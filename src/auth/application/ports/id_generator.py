from abc import ABC, abstractmethod

from auth.domain.session.session_id import SessionId
from auth.domain.shared.event_id import EventId
from auth.domain.user.user_id import UserId


class IdGenerator(ABC):
    @abstractmethod
    def generate_user_id(self) -> UserId: ...
    @abstractmethod
    def generate_event_id(self) -> EventId: ...
    @abstractmethod
    def generate_session_id(self) -> SessionId: ...
