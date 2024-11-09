import abc

from fastapi import BackgroundTasks


from running_app.running.running_state.application.port.input.command.snapshot_running_status_command import (
    SnapshotRunningStateCommand,
)
from running_app.running.running_state.domain.model.current_run import CurrentRun
from running_app.running.running_state.domain.running_state import RunningState


class CreateRunningStatusUseCase(abc.ABC):
    """Create running status use case interface."""

    @abc.abstractmethod
    async def snapshot_running_state(
        self, background_tasks: BackgroundTasks, command: SnapshotRunningStateCommand
    ) -> CurrentRun:
        """Create running status. And return current left percentage, and current target path coordinate"""
