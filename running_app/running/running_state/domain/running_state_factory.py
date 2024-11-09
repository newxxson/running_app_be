import datetime
import uuid


from running_app.running.running_state.domain.model.current_run import CurrentRun
from running_app.running.running_state.domain.running_state import RunningState


class RunningStateFactory:
    """Running state factory."""

    @staticmethod
    def create_running_state(
        current_run: CurrentRun,
        time: datetime.datetime,
        latitude: float,
        longitude: float,
    ) -> RunningState:
        """Create running state."""
        return RunningState(
            identifier=uuid.uuid4(),
            run_identifier=current_run.run_identifier,
            runner_identifier=current_run.runner_identifier,
            time=time,
            latitude=latitude,
            longitude=longitude,
            speed=current_run.calculate_speed(latitude, longitude, time),
        )
