import abc
import msgspec

from running_app.path.domain.coordinate import Coordinate


class SaveCoordinateOutput(abc.ABC):
    """Save coordinate output interface."""

    @abc.abstractmethod
    async def save_all(self, coordinates: list[Coordinate]) -> None:
        """Save all coordinates."""
