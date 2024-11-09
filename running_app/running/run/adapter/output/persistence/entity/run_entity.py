import datetime
from uuid import UUID
import uuid

from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    ForeignKey,
    Index,
    String,
    TypeDecorator,
    Uuid,
)
from running_app.common.database.base_model import Base
from sqlalchemy.orm import mapped_column, Mapped

from running_app.running.run.domain.enum.running_status import RunningStatus
from running_app.running.run.domain.run import Run


class UUIDListType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, dialect):
        # Convert list of UUIDs to list of strings before saving to the database
        if value is not None:
            return [str(item) for item in value]
        return value

    def process_result_value(self, value, dialect):
        # Convert list of strings back to list of UUIDs after retrieving from the database
        if value is not None:
            return [uuid.UUID(item) for item in value]
        return value


class RunEntity(Base):
    """Run entity."""

    __tablename__ = "run"
    __table_args__ = (
        Index("run_user_identifier_idx", "user_identifier"),
        Index("run_crew_identifier_idx", "crew_identifier"),
    )

    identifier: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    running_status: Mapped[RunningStatus] = mapped_column(String, nullable=False)

    user_identifier: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), nullable=True
    )
    crew_identifier: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), nullable=True
    )

    running_user_identifiers: Mapped[list[UUID]] = mapped_column(
        UUIDListType, nullable=False
    )

    total_distance: Mapped[float] = mapped_column(Float, nullable=False)

    path_identifier: Mapped[UUID] = mapped_column(
        ForeignKey("path.identifier"), nullable=False
    )

    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    @classmethod
    def from_domain(cls, run: Run) -> "RunEntity":
        """Create run entity from domain."""
        return cls(
            identifier=run.identifier,
            title=run.title,
            description=run.description,
            running_status=run.running_status.value,
            user_identifier=run.user_identifier,
            crew_identifier=run.crew_identifier,
            running_user_identifiers=run.running_user_identifiers,
            total_distance=run.total_distance,
            path_identifier=run.path_identifier,
            created_date=run.created_date,
        )

    def to_domain(self) -> Run:
        """Convert to domain."""
        return Run(
            identifier=self.identifier,
            title=self.title,
            description=self.description,
            running_status=RunningStatus(self.running_status),
            user_identifier=self.user_identifier,
            crew_identifier=self.crew_identifier,
            running_user_identifiers=self.running_user_identifiers,
            total_distance=self.total_distance,
            path_identifier=self.path_identifier,
            created_date=self.created_date,
        )
