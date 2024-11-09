import abc

from running_app.path.application.input.command.register_corrdinate_command import (
    RegisterCoordinateCommand,
)


class RegisterCoordinateUseCase(abc.ABC):
    """Register coordinate use case interface."""

    @abc.abstractmethod
    async def register_coordinate(
        self, register_coordinate_command: RegisterCoordinateCommand
    ) -> None:
        """Register coordinate."""
