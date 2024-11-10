import datetime
from typing import Self
from uuid import UUID


from sqlalchemy import DateTime, Float, ForeignKey, String, Uuid
from running_app.common.database.base_model import Base
from sqlalchemy.orm import mapped_column, Mapped
from running_app.path.domain.path import Path


class PathEntity(Base):
    """런닝 경로 엔티티입니다."""

    __tablename__ = "path"

    identifier: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    total_distance: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_required_minute: Mapped[float] = mapped_column(Float, nullable=False)

    creator_identifier: Mapped[UUID] = mapped_column(
        ForeignKey("user.identifier"), nullable=False
    )

    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    last_modified_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    @classmethod
    def from_domain(cls, path: Path) -> Self:
        """도메인 객체를 엔티티 객체로 변환합니다."""
        return cls(
            identifier=path.identifier,
            title=path.title,
            description=path.description,
            total_distance=path.total_distance,
            estimated_required_minute=path.estimated_required_minute,
            creator_identifier=path.creator_identifier,
            created_date=path.created_date,
            last_modified_date=path.last_modified_date,
        )

    def to_domain(self) -> Path:
        """엔티티 객체를 도메인 객체로 변환합니다."""
        return Path(
            identifier=self.identifier,
            title=self.title,
            description=self.description,
            total_distance=self.total_distance,
            estimated_required_minute=self.estimated_required_minute,
            creator_identifier=self.creator_identifier,
            created_date=self.created_date,
            last_modified_date=self.last_modified_date,
        )
