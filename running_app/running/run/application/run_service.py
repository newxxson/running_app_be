from sys import path_hooks
from injector import inject
from running_app.common.database.db_context import DBContext
from running_app.path.domain.exception.path_not_found_exception import (
    PathNotFoundException,
)
from running_app.running.run.application.input.command.create_run_command import (
    CreateRunCommand,
)
from running_app.running.run.application.input.command.update_run_command import (
    UpdateRunCommand,
)
from running_app.running.run.application.input.usecase.create_run_usecase import (
    CreateRunUseCase,
)
from running_app.running.run.application.input.usecase.update_run_usecase import (
    UpdateRunUseCase,
)
from running_app.running.run.application.output.find_path_output import (
    RunFindPathOutput,
)
from running_app.running.run.application.output.find_run_output import FindRunOutput
from running_app.running.run.application.output.save_run_output import SaveRunOutput
from running_app.running.run.domain.exception.run_not_found_exception import (
    RunNotFoundException,
)
from running_app.running.run.domain.run import Run
from running_app.running.run.domain.run_factory import RunFactory


class RunService(CreateRunUseCase, UpdateRunUseCase):
    """Run service."""

    @inject
    def __init__(
        self,
        db_context: DBContext,
        find_run_output: FindRunOutput,
        save_run_output: SaveRunOutput,
        find_path_output: RunFindPathOutput,
    ) -> None:
        self.db_context = db_context
        self.find_run_output = find_run_output
        self.save_run_output = save_run_output
        self.find_path_output = find_path_output

    async def update_run(self, update_run_command: UpdateRunCommand) -> Run:
        """Update run."""
        async with self.db_context.begin_transaction(read_only=True):
            run = await self.find_run_output.find_run_by_id(
                run_identifier=update_run_command.identifier
            )

        if not run:
            raise RunNotFoundException(run_identifier=update_run_command.identifier)

        run.update(
            title=update_run_command.title,
            description=update_run_command.description,
            running_status=update_run_command.running_status,
            user_identifier=update_run_command.user_identifier,
            crew_identifier=update_run_command.crew_identifier,
            running_user_identifiers=update_run_command.running_user_identifiers,
        )
        async with self.db_context.begin_transaction(read_only=False):
            await self.save_run_output.save_run(run)

        return run

    async def create_run(self, create_run_command: CreateRunCommand) -> Run:
        """Create run."""
        async with self.db_context.begin_transaction(read_only=True):
            path = await self.find_path_output.find_path_by_id(
                path_identifier=create_run_command.path_identifier
            )
        if not path:
            raise PathNotFoundException(
                path_identifier=create_run_command.path_identifier
            )

        run = RunFactory.create_run(create_run_command=create_run_command, path=path)

        async with self.db_context.begin_transaction(read_only=False):
            await self.save_run_output.save_run(run)

        return run
