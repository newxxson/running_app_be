import datetime
from uuid import UUID

from geoalchemy2 import Geography
from running_app.common.database.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, ForeignKey, Uuid


class RunningStateEntity(Base):
    """RunningState entity."""

    __tablename__ = "running_state"

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
