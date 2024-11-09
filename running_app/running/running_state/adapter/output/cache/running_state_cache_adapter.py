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

        return msgspec.convert(result, CurrentRun) if result else None

    async def save_current_run(self, current_run: CurrentRun) -> None:
        """Save current run."""
        key = f"{current_run.run_identifier}:{current_run.runner_identifier}"
        await self.cache_manager.set_cache(
            key=key, mapping=msgspec.to_builtins(current_run)
        )
