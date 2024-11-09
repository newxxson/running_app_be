import abc

from running_app.crew.application.accept_invite_command import AcceptInviteCommand
from running_app.crew.domain.crew_invite import CrewInvite


class AcceptInviteUseCase(abc.ABC):
    
    @abc.abstractmethod
    async def accept_invite(self, command: AcceptInviteCommand) -> CrewInvite:
        """Accept invite."""
    
