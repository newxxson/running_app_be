import abc

from running_app.crew.domain.crew import Crew


class CreateCrewUseCase(abc.ABC):
    """Create crew use case."""

    @abc.abstractmethod
    async def create_crew(self, crew_name: str) -> Crew:
        """Create crew."""
