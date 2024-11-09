import abc

from running_app.path.application.input.command.create_path_command import (
    CreatePathCommand,
)
from running_app.path.domain.path import Path


class CreatePathUseCase(abc.ABC):
    """Create path use case interface."""

    @abc.abstractmethod
    async def create_path(self, create_path_command: CreatePathCommand) -> Path:
        """Create path."""
