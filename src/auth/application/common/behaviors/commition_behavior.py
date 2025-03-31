from bazario.asyncio import HandleNext, PipelineBehavior

from auth.application.common.markers.command import Command
from auth.application.ports.committer import Committer


class CommitionBehavior[C: Command, R](PipelineBehavior[C, R]):
    def __init__(self, committer: Committer) -> None:
        self._committer = committer

    async def handle(self, request: C, handle_next: HandleNext[C, R]) -> R:
        response = await handle_next(request)

        await self._committer.commit()

        return response
