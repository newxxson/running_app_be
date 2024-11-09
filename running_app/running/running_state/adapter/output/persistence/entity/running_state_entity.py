import datetime
from uuid import UUID

from geoalchemy2 import Geography, WKTElement
from geoalchemy2.shape import from_shape
from shapely import Point
from running_app.common.database.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Float, ForeignKey, Index, Uuid

from running_app.running.running_state.domain.running_state import RunningState


class RunningStateEntity(Base):
    """RunningState entity."""

    __tablename__ = "running_state"
    __table_args__ = (
        Index(
            "running_state_run_identifier_runner_identifier_idx",
            "run_identifier",
            "runner_identifier",
        ),
        Index(
            "running_state_run_identifier_idx",
            "run_identifier",
        ),
    )

    identifier: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)

    run_identifier: Mapped[UUID] = mapped_column(
        ForeignKey("run.identifier"), nullable=False
    )

    runner_identifier: Mapped[UUID] = mapped_column(
        ForeignKey("user.identifier"), nullable=False
    )

    time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    location = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )

    speed: Mapped[float] = mapped_column(Float, nullable=False)

    @classmethod
    def from_domain(cls, running_state: RunningState) -> "RunningStateEntity":
        location = WKTElement(
            f"POINT({running_state.longitude} {running_state.latitude})", srid=4326
        )

        return cls(
            identifier=running_state.identifier,
            run_identifier=running_state.run_identifier,
            runner_identifier=running_state.runner_identifier,
            time=running_state.time,
            location=location,
            speed=running_state.speed,
        )
