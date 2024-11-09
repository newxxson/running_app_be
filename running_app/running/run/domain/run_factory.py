import datetime
import uuid
from running_app.path.domain.path import Path
from running_app.running.run.application.input.command.create_run_command import (
    CreateRunCommand,
)
from running_app.running.run.domain.run import Run


class RunFactory:
    """Run factory."""

    @staticmethod
    def create_run(create_run_command: CreateRunCommand, path: Path) -> Run:
        """Create run."""
        return Run(
            identifier=uuid.uuid4(),
            title=create_run_command.title,
            description=create_run_command.description,
            running_status=create_run_command.running_status,
            user_identifier=create_run_command.user_identifier,
            crew_identifier=create_run_command.crew_identifier,
            running_user_identifiers=create_run_command.running_user_identifiers,
            path_identifier=path.identifier,
            total_distance=path.total_distance,
            created_date=datetime.datetime.now(tz=datetime.UTC),
        )
