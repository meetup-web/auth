from abc import ABC, abstractmethod

from auth.domain.user.user import User
from auth.domain.user.user_id import UserId


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None: ...
    @abstractmethod
    async def delete(self, user: User) -> None: ...
    @abstractmethod
    async def with_id(self, user_id: UserId) -> User | None: ...
    @abstractmethod
    async def with_username(self, username: str) -> User | None: ...
