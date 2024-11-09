from uuid import UUID
from sqlalchemy import String, Uuid, ForeignKey, DateTime, Boolean
from running_app.common.database.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from running_app.crew.domain.enum.role import CrewRole
from injector import inject
from sqlalchemy import select
from running_app.common.database.db_context import DBContext
from running_app.crew.domain.crew import Crew
from running_app.crew.domain.crew_invite import CrewInvite
from typing import Self


class CrewEntity(Base):
    """Crew entity."""

    __tablename__ = "crew"

    identifier: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    crew_name: Mapped[str] = mapped_column(String, nullable=False)

    members = relationship("CrewMemberEntity", back_populates="crew")

    @classmethod
    def of(cls, crew: Crew) -> Self:
        """Create user entity from user domain object."""
        return cls(
            identifier=crew.identifier,
            crew_name=crew.crew_name,
        )

    def to_domain(self) -> Crew:
        """Convert user entity to user domain object."""
        return Crew(
            identifier=self.identifier,
            crew_name=self.crew_name,
            members=self.members,
        )

class CrewMemberEntity(Base):
    """Crew member entity."""

    __tablename__ = "crew_member"

    user_identifier: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    crew_identifier: Mapped[UUID] = mapped_column(ForeignKey("crew.identifier"))
    joined_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    role: Mapped[CrewRole] = mapped_column(String, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    crew = relationship("CrewEntity", back_populates="members")


class CrewInviteEntity(Base):
    """Crew invite entity."""

    __tablename__ = "crew_invite"

    request_identifier: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    crew_identifier: Mapped[UUID] = mapped_column(ForeignKey("crew.identifier"))
    user_identifier: Mapped[UUID] = mapped_column(ForeignKey("user.identifier"))
    invited_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False)

    @classmethod
    def of(cls, invite: CrewInvite) -> Self:
        """Create user entity from user domain object."""
        return cls(
            request_identifier=invite.request_identifier,
            crew_identifier=invite.crew_identifier,
            user_identifier=invite.user_identifier,
            invited_at=invite.invited_at,
            status=invite.status,
            is_deleted=invite.is_deleted,
        )

    def to_domain(self) -> CrewInvite:
        """Convert user entity to user domain object."""
        return CrewInvite(
            request_identifier=self.request_identifier,
            crew_identifier=self.crew_identifier,
            user_identifier=self.user_identifier,
            invited_at=self.invited_at,
            status=self.status,
            is_deleted=self.is_deleted,
        )

class CrewRepository:
    """Crew repository.""" 

    @inject
    def __init__(self, db_context: DBContext) -> None:
        self.db_context = db_context

    async def find_by_id(self, identifier: UUID) -> Crew | None:
        """Find crew by id."""
        statement = select(CrewEntity).where(CrewEntity.identifier == identifier)

        result = await self.db_context.session.execute(statement)

        crew_entity = result.scalars().first()

        return crew_entity.to_domain() if crew_entity else None

    async def save_invite(self, invite: CrewInvite) -> CrewInvite:
        """Save invite."""
        invite_entity = CrewInviteEntity.of(invite)
        self.db_context.session.add(invite_entity)

        await self.db_context.session.flush()

        return invite_entity.to_domain()