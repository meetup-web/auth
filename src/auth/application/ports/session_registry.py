from abc import ABC, abstractmethod

from auth.application.models.session import SessionReadModel


class SessionRegistry(ABC):
    @abstractmethod
    def set_session(self, session: SessionReadModel) -> None: ...
    @abstractmethod
    def raise_session(self) -> SessionReadModel | None: ...
