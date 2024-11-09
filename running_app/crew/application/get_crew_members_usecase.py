import abc

from running_app.crew.application.get_crew_members_command import GetCrewMembersCommand
from running_app.crew.adapter.response import CrewMembersResponse



class GetCrewMembersUseCase(abc.ABC):
    
    @abc.abstractmethod
    async def get_crew_members(self, command: GetCrewMembersCommand) -> CrewMembersResponse:
        """Get crew members."""
