import datetime
from uuid import UUID

from injector import inject
import msgspec
from running_app.common.cache.cache import CacheManager
from running_app.running.running_state.application.port.output.find_current_run_output import (
    FindCurrentRunOutput,
)
from running_app.running.running_state.application.port.output.save_current_run_output import (
    SaveCurrentRunOutput,
)
from running_app.running.running_state.domain.model.current_run import CurrentRun
from running_app.common.log import logger


class RunningStateCacheAdapter(SaveCurrentRunOutput, FindCurrentRunOutput):
    """Running state cache adapter."""

    @inject
    def __init__(self, cache_manager: CacheManager) -> None:
        self.cache_manager = cache_manager

    async def find_current_run_by_run_id_and_user_id(
        self, run_identifier: UUID, runner_identifier: UUID
    ) -> CurrentRun | None:
        """Find current run by run id and user id."""
        key = f"{run_identifier}:{runner_identifier}"
        result = await self.cache_manager.get_cache(key=key)

        logger.info(f"Find current run from cache: {result}")

        if result:
            ctcl = result.get("current_target_coordinate_latitude")
            ctclo = result.get("current_target_coordinate_longitude")
            speed = result.get("speed")
            if speed:
                speed = float(speed)
            else:
                speed = 0

            max_sequence = result.get("max_sequence")
            max_sequence = int(max_sequence) if max_sequence else 0

            current_sequence = result.get("current_sequence")
            current_sequence = int(current_sequence) if current_sequence else 0

            return CurrentRun(
                run_identifier=UUID(result["run_identifier"]),
                runner_identifier=UUID(result["runner_identifier"]),
                path_identifier=UUID(result["path_identifier"]),
                latitude=float(result["latitude"]),
                longitude=float(result["longitude"]),
                current_sequence=current_sequence,
                speed=speed,
                time=datetime.datetime.fromisoformat(result["time"]),
                max_sequence=max_sequence,
                current_target_coordinate_latitude=float(ctcl) if ctcl else None,
                current_target_coordinate_longitude=float(ctclo) if ctclo else None,
            )

    async def save_current_run(self, current_run: CurrentRun) -> None:
        """Save current run."""
        key = f"{current_run.run_identifier}:{current_run.runner_identifier}"

        mappings = msgspec.to_builtins(current_run)

        mappings["time"] = current_run.time.isoformat()

        await self.cache_manager.set_cache(
            key=key, mapping=msgspec.to_builtins(current_run)
        )
