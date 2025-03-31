from datetime import datetime

from auth.domain.shared.entity import Entity
from auth.domain.shared.events import DomainEventAdder
from auth.domain.user.events import (
    UsernameChanged,
    UserPasswordChanged,
)
from auth.domain.user.user_id import UserId


class User(Entity[UserId]):
    def __init__(
        self,
        entity_id: UserId,
        event_adder: DomainEventAdder,
        *,
        password: bytes,
        username: str,
        created_at: datetime,
    ) -> None:
        Entity.__init__(self, entity_id, event_adder)

        self._password = password
        self._username = username
        self._created_at = created_at

    def change_username(self, username: str, current_date: datetime) -> None:
        if self._username == username:
            return

        self._username = username
        event = UsernameChanged(
            user_id=self._entity_id, username=username, event_date=current_date
        )

        self.add_event(event)

    def change_password(self, password: bytes, current_date: datetime) -> None:
        self._password = password
        event = UserPasswordChanged(
            user_id=self._entity_id, password=password, event_date=current_date
        )

        self.add_event(event)

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> bytes:
        return self._password

    @property
    def created_at(self) -> datetime:
        return self._created_at
