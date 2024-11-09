from uuid import UUID

from injector import inject
from sqlalchemy import select
from running_app.common.database.db_context import DBContext
from running_app.running.run.adapter.output.persistence.entity.run_entity import (
    RunEntity,
)
from running_app.running.run.application.output.find_run_output import FindRunOutput
from running_app.running.run.application.output.save_run_output import SaveRunOutput
from running_app.running.run.domain.run import Run


class RunPersistenceAdapter(FindRunOutput, SaveRunOutput):
    """Run persistence adapter."""

    @inject
    def __init__(self, db_context: DBContext) -> None:
        self.db_context = db_context

    async def save_run(self, run: Run) -> None:
        """Save run."""
        await self.db_context.session.merge(RunEntity.from_domain(run))

    async def find_run_by_id(self, run_identifier: UUID) -> Run | None:
        """Find run by id."""
        statement = select(RunEntity).where(RunEntity.identifier == run_identifier)

        result = await self.db_context.session.execute(statement)
        run_entity = result.scalars().first()

        return run_entity.to_domain() if run_entity else None
