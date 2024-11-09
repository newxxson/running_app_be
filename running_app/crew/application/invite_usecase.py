import abc

from running_app.crew.application.invite_command import InviteCommand
from running_app.crew.adapter.response import CrewInviteResponse


class InviteUseCase(abc.ABC):
    
    @abc.abstractmethod
    async def invite(self,  command: InviteCommand) -> CrewInviteResponse:
        """Invite."""
    
