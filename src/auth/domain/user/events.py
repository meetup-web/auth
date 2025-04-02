from dataclasses import dataclass

from auth.domain.shared.events import DomainEvent
from auth.domain.user.user_id import UserId


@dataclass(frozen=True)
class UserCreated(DomainEvent):
    user_id: UserId
    username: str
    password: bytes


@dataclass(frozen=True)
class UserDeleted(DomainEvent):
    user_id: UserId


@dataclass(frozen=True)
class UsernameChanged(DomainEvent):
    user_id: UserId
    username: str


@dataclass(frozen=True)
class UserPasswordChanged(DomainEvent):
    user_id: UserId
    password: bytes
