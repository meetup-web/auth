from datetime import datetime

from auth.domain.session.session_id import SessionId
from auth.domain.shared.entity import Entity
from auth.domain.shared.events import DomainEventAdder
from auth.domain.user.user_id import UserId


class Session(Entity[SessionId]):
    def __init__(
        self,
        entity_id: SessionId,
        event_adder: DomainEventAdder,
        *,
        user_id: UserId,
        expires_at: datetime,
    ) -> None:
        Entity.__init__(self, entity_id, event_adder)

        self._user_id = user_id
        self._expires_at = expires_at

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def expires_at(self) -> datetime:
        return self._expires_at
