from uuid import UUID
from sqlalchemy import String, Uuid, ForeignKey, DateTime, Boolean
from running_app.common.database.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from running_app.crew.adapter.response import CrewMemberResponse
from running_app.crew.domain.enum.role import CrewRole
from injector import inject
from sqlalchemy import select, update
from running_app.common.database.db_context import DBContext
from running_app.crew.domain.crew import Crew
from typing import Self
from running_app.crew.domain.enum.status import CrewMemberStatus
from running_app.crew.domain.crew_member import CrewMember
from running_app.user.adapter.output.persistence.entity.user_entity import UserEntity


class CrewEntity(Base):
    """Crew entity."""

    __tablename__ = "crew"

    identifier: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    crew_name: Mapped[str] = mapped_column(String, nullable=False)

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
        )


class CrewMemberEntity(Base):
    """Crew member entity."""

    __tablename__ = "crew_member"

    identifier: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    user_identifier: Mapped[UUID] = mapped_column(ForeignKey("user.identifier"))
    crew_identifier: Mapped[UUID] = mapped_column(ForeignKey("crew.identifier"))
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    role: Mapped[CrewRole] = mapped_column(String, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    member_status: Mapped[CrewMemberStatus] = mapped_column(String, nullable=False)

    @classmethod
    def of(cls, member: CrewMember) -> Self:
        """Create user entity from user domain object."""
        return cls(
            identifier=member.identifier,
            user_identifier=member.user_identifier,
            crew_identifier=member.crew_identifier,
            joined_at=member.joined_at,
            role=member.role.value,
            member_status=member.member_status.value,
            is_deleted=member.is_deleted,
        )

    def to_domain(self) -> CrewMember:
        """Convert user entity to user domain object."""
        return CrewMember(
            identifier=self.identifier,
            user_identifier=self.user_identifier,
            crew_identifier=self.crew_identifier,
            joined_at=self.joined_at,
            role=CrewRole(self.role),
            member_status=CrewMemberStatus(self.member_status),
            is_deleted=self.is_deleted,
        )


class CrewRepository:
    """Crew repository."""

    @inject
    def __init__(self, db_context: DBContext) -> None:
        self.db_context = db_context

    async def find_by_id(self, identifier: UUID) -> Crew | None:
        """Find crew by id."""
        stmt = select(CrewEntity).where(CrewEntity.identifier == identifier)

        result = await self.db_context.session.execute(stmt)

        crew_entity = result.scalars().first()

        return crew_entity.to_domain() if crew_entity else None

    async def create_member(self, member: CrewMember) -> None:
        """Save member."""
        member_entity = CrewMemberEntity.of(member)
        self.db_context.session.add(member_entity)

        await self.db_context.session.flush()

        return

    async def create(self, crew: Crew) -> None:
        """Save crew."""
        crew_entity = CrewEntity.of(crew)
        self.db_context.session.add(crew_entity)

        await self.db_context.session.flush()

    async def find_member_by_id(self, identifier: UUID) -> CrewMember | None:
        stmt = select(CrewMemberEntity).where(CrewMemberEntity.identifier == identifier)

        result = await self.db_context.session.execute(stmt)

        member_entity = result.scalars().first()

        return member_entity.to_domain() if member_entity else None

    async def update_member(self, member: CrewMember) -> None:
        """Update crew member."""
        await self.db_context.session.merge(CrewMemberEntity.of(member))

    async def find_member_by_user_id_and_crew_id(
        self, user_identifier: UUID, crew_identifier: UUID
    ) -> CrewMember | None:
        stmt = select(CrewMemberEntity).where(
            CrewMemberEntity.user_identifier == user_identifier,
            CrewMemberEntity.crew_identifier == crew_identifier,
        )

        result = await self.db_context.session.execute(stmt)

        member_entity = result.scalars().first()

        return member_entity.to_domain() if member_entity else None

    async def find_by_user_id(self, user_identifier: UUID) -> UUID | None:
        stmt = select(CrewMemberEntity).where(
            CrewMemberEntity.user_identifier == user_identifier
        )

        result = await self.db_context.session.execute(stmt)

        crew_member_entity = result.scalars().first()

        return crew_member_entity.crew_identifier if crew_member_entity else None

    async def find_members_by_crew_id(
        self, crew_identifier: UUID
    ) -> list[CrewMemberResponse]:
        stmt = (
            select(UserEntity.identifier, UserEntity.nickname, UserEntity.gender)
            .join(
                CrewMemberEntity,
                CrewMemberEntity.user_identifier == UserEntity.identifier,
            )
            .where(CrewMemberEntity.crew_identifier == crew_identifier)
        )

        result = await self.db_context.session.execute(stmt)

        return [
            CrewMemberResponse(
                identifier=row.identifier, nickname=row.nickname, gender=row.gender
            )
            for row in result.all()
        ]

    async def find_crew_member_by_user_id_and_status(
        self, user_identifier: UUID, status: CrewMemberStatus
    ) -> list[CrewMember]:
        stmt = select(CrewMemberEntity).where(
            CrewMemberEntity.user_identifier == user_identifier,
            CrewMemberEntity.member_status == status.value,
        )

        result = await self.db_context.session.execute(stmt)

        crew_members = result.scalars().all()

        return [member.to_domain() for member in crew_members]
