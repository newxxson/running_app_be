import abc
from uuid import UUID

from running_app.crew.domain.crew import Crew
from running_app.crew.domain.crew_member import CrewMember
from running_app.crew.domain.enum.status import CrewMemberStatus


class QueryCrewUseCase(abc.ABC):
    """Query crew members use case interface."""

    @abc.abstractmethod
    async def find_crew_member_by_user_id_and_status(
        self, user_identifier: UUID, status: CrewMemberStatus
    ) -> list[CrewMember]:
        """Find crew members by crew identifier."""

    @abc.abstractmethod
    async def find_crews(self) -> list[Crew]:
        """Find crews."""
