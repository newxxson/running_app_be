from uuid import UUID
from geoalchemy2 import Geometry
from injector import inject
from sqlalchemy import cast, func, select
from running_app.common.database.db_context import DBContext
from running_app.running.running_state.adapter.output.persistence.entity.running_state_entity import (
    RunningStateEntity,
)
from running_app.running.running_state.application.port.output.find_running_state_output import (
    FindRunningStateOutput,
)
from running_app.running.running_state.application.port.output.save_running_state_output import (
    SaveRunningStateOutput,
)
from running_app.running.running_state.domain.running_state import RunningState


class RunningStatePersistenceAdapter(SaveRunningStateOutput, FindRunningStateOutput):
    """Running state persistence adapter."""

    @inject
    def __init__(self, db_context: DBContext) -> None:
        self.db_context = db_context

    async def save_running_state(self, running_state: RunningState) -> None:
        """Save running state."""
        await self.db_context.session.merge(
            RunningStateEntity.from_domain(running_state)
        )

    async def find_running_state_by_run_identifier(
        self, run_identifier: UUID
    ) -> list[RunningState]:
        """Find running state by run identifier."""
        statement = select(
            RunningStateEntity.identifier,
            RunningStateEntity.run_identifier,
            RunningStateEntity.runner_identifier,
            RunningStateEntity.time,
            func.ST_X(cast(RunningStateEntity.location, Geometry)).label("longitude"),
            func.ST_Y(cast(RunningStateEntity.location, Geometry)).label("latitude"),
            RunningStateEntity.speed,
        ).where(RunningStateEntity.run_identifier == run_identifier)

        result = await self.db_context.session.execute(statement)

        return [
            RunningState(
                identifier=row.identifier,
                run_identifier=row.run_identifier,
                runner_identifier=row.runner_identifier,
                time=row.time,
                latitude=row.latitude,
                longitude=row.longitude,
                speed=row.speed,
            )
            for row in result.all()
        ]
