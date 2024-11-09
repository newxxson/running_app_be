from os import path
from fastapi import BackgroundTasks
from injector import inject
from running_app.common.database.db_context import DBContext

from running_app.path.domain.exception.path_not_found_exception import (
    PathNotFoundException,
)
from running_app.running.run.domain.exception.run_not_found_exception import (
    RunNotFoundException,
)
from running_app.running.running_state.application.port.input.command.snapshot_running_status_command import (
    SnapshotRunningStateCommand,
)
from running_app.running.running_state.application.port.input.create_running_status_usecase import (
    CreateRunningStatusUseCase,
)
from running_app.running.running_state.application.port.output.find_current_run_output import (
    FindCurrentRunOutput,
)
from running_app.running.running_state.application.port.output.find_path_coordinate_output import (
    RunningStateFindPathCoordinateOutput,
)
from running_app.running.running_state.application.port.output.find_run_output import (
    RunningStateFindRunOutput,
)
from running_app.running.running_state.application.port.output.save_current_run_output import (
    SaveCurrentRunOutput,
)
from running_app.running.running_state.application.port.output.save_running_state_output import (
    SaveRunningStateOutput,
)
from running_app.running.running_state.domain.model.current_run import CurrentRun
from running_app.running.running_state.domain.running_state_factory import (
    RunningStateFactory,
)


class RunningStateService(CreateRunningStatusUseCase):
    """Running state service."""

    @inject
    def __init__(
        self,
        db_context: DBContext,
        find_current_run_output: FindCurrentRunOutput,
        find_run_output: RunningStateFindRunOutput,
        find_path_coordinate_output: RunningStateFindPathCoordinateOutput,
        save_current_run_output: SaveCurrentRunOutput,
        save_running_state_output: SaveRunningStateOutput,
    ) -> None:
        self.db_context = db_context
        self.find_current_run_output = find_current_run_output
        self.find_run_output = find_run_output
        self.find_path_coordinate_output = find_path_coordinate_output
        self.save_current_run_output = save_current_run_output
        self.save_running_state_output = save_running_state_output

    async def snapshot_running_state(
        self, background_tasks: BackgroundTasks, command: SnapshotRunningStateCommand
    ) -> CurrentRun:
        """Create running status. And return current left percentage, and current target path coordinate"""
        # 캐시로부터 현재 진행중인 러닝을 찾습니다.
        ongoing_run = (
            await self.find_current_run_output.find_current_run_by_run_id_and_user_id(
                run_identifier=command.run_identifier,
                runner_identifier=command.runner_identifier,
            )
        )
        if not ongoing_run:
            # 첫 런닝 상태를 생성합니다.
            async with self.db_context.begin_transaction(read_only=True):
                run = await self.find_run_output.find_run_by_run_id(
                    run_identifier=command.run_identifier
                )
                if not run:
                    raise RunNotFoundException(run_identifier=command.run_identifier)

                max_sequence = await self.find_path_coordinate_output.count_path_coordinates_by_path_id(
                    path_identifier=run.path_identifier
                )

                current_target_coordinate = await self.find_path_coordinate_output.find_path_coordinate_by_path_id_and_sequence(
                    path_identifier=run.path_identifier, sequence=1
                )

                if not path:
                    raise PathNotFoundException(path_identifier=run.path_identifier)

            ongoing_run = CurrentRun(
                run_identifier=command.run_identifier,
                runner_identifier=command.runner_identifier,
                path_identifier=run.path_identifier,
                latitude=command.latitude,
                longitude=command.longitude,
                speed=0,
                time=command.time,
                current_sequence=0,
                max_sequence=max_sequence,
                current_target_coordinate_latitude=current_target_coordinate.latitude
                if current_target_coordinate
                else None,
                current_target_coordinate_longitude=current_target_coordinate.longitude
                if current_target_coordinate
                else None,
            )

        new_running_state = RunningStateFactory.create_running_state(
            current_run=ongoing_run,
            time=command.time,
            latitude=command.latitude,
            longitude=command.longitude,
        )

        if (
            ongoing_run.is_target_coordinate_reached(
                new_latitude=command.latitude,
                new_longitude=command.longitude,
            )
            and ongoing_run.path_identifier
        ):
            # 다음 좌표를 찾습니다.
            next_sequence = ongoing_run.current_sequence + 1
            next_coordinate = await self.find_path_coordinate_output.find_path_coordinate_by_path_id_and_sequence(
                path_identifier=ongoing_run.path_identifier, sequence=next_sequence
            )

            if next_coordinate:
                # current_run 의 target_coordinate 를 업데이트 합니다.
                ongoing_run.update_current_run(
                    new_latitude=command.latitude,
                    new_longitude=command.longitude,
                    new_time=command.time,
                    coordinate=next_coordinate,
                )
                background_tasks.add_task(
                    self.save_current_run_output.save_current_run,
                    current_run=ongoing_run,
                )

        # 현재 러닝 상태를 저장합니다.
        background_tasks.add_task(
            self.save_running_state_output.save_running_state,
            running_state=new_running_state,
        )

        return ongoing_run
