from abc import ABC, abstractmethod

from auth.domain.session.session import Session
from auth.domain.user.user_id import UserId


class SessionFactory(ABC):
    @abstractmethod
    def create_session(self, user_id: UserId) -> Session: ...
