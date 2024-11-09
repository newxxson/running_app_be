from injector import inject
from running_app.common.database.db_context import DBContext
from running_app.running.running_state.adapter.output.persistence.entity.running_state_entity import (
    RunningStateEntity,
)
from running_app.running.running_state.application.port.output.save_running_state_output import (
    SaveRunningStateOutput,
)
from running_app.running.running_state.domain.running_state import RunningState


class RunningStatePersistenceAdapter(SaveRunningStateOutput):
    """Running state persistence adapter."""

    @inject
    def __init__(self, db_context: DBContext) -> None:
        self.db_context = db_context

    async def save_running_state(self, running_state: RunningState) -> None:
        """Save running state."""
        await self.db_context.session.merge(
            RunningStateEntity.from_domain(running_state)
        )
