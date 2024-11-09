import abc

from running_app.crew.application.invite_command import InviteCommand
from running_app.crew.domain.crew_invite import CrewInvite



class InviteUseCase(abc.ABC):
    
    @abc.abstractmethod
    async def invite(self,  command: InviteCommand) -> CrewInvite:
        """Invite."""
    
