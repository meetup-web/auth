from auth.application.models.session import SessionReadModel
from auth.application.ports.session_registry import SessionRegistry


class WebSessionRegistry(SessionRegistry):
    def __init__(self) -> None:
        self._session: SessionReadModel | None = None

    def set_session(self, session: SessionReadModel) -> None:
        if self._session is not None:
            raise KeyError("Session already exists")

        self._session = session

    def raise_session(self) -> SessionReadModel | None:
        return self._session
