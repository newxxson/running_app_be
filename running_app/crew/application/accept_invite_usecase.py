import abc

from running_app.crew.application.accept_invite_command import AcceptInviteCommand
from fastapi import Response


class AcceptInviteUseCase(abc.ABC):
    
    @abc.abstractmethod
    async def accept_invite(self, command: AcceptInviteCommand) -> Response:
        """Accept invite."""
    
