from dataclasses import dataclass

from bazario import Request


@dataclass(frozen=True)
class Query[TRes](Request[TRes]): ...
