from dataclasses import dataclass

from auth.domain.user.user_id import UserId


@dataclass(frozen=True)
class UserReadModel:
    user_id: UserId
    username: str
