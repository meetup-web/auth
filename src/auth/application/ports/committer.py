from abc import ABC, abstractmethod


class Committer(ABC):
    @abstractmethod
    async def commit(self) -> None: ...
