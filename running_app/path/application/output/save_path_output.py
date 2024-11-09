import abc
from running_app.path.domain.path import Path


class SavePathOutput(abc.ABC):
    """Save path output interface."""

    @abc.abstractmethod
    async def save_path(self, path: Path) -> None:
        """Save path."""
