from typing import Self
from uuid import UUID
from sqlalchemy import String, Uuid
from running_app.common.database.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column
from running_app.user.domain.enum.gender import Gender
from running_app.user.domain.user import User


class UserEntity(Base):
    """User entity."""

    __tablename__ = "user"

    identifier: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    kakao_id: Mapped[str] = mapped_column(String, nullable=False)

    nickname: Mapped[str] = mapped_column(String, nullable=False)

    gender: Mapped[Gender] = mapped_column(String, nullable=False)

    profile_image_url: Mapped[str | None] = mapped_column(String, nullable=True)

    @classmethod
    def of(cls, user: User) -> Self:
        """Create user entity from user domain object."""
        return cls(
            identifier=user.identifier,
            kakao_id=user.kakao_id,
            nickname=user.nickname,
            gender=user.gender,
            profile_image_url=user.profile_image_url,
        )

    def to_domain(self) -> User:
        """Convert user entity to user domain object."""
        return User(
            identifier=self.identifier,
            kakao_id=self.kakao_id,
            nickname=self.nickname,
            gender=self.gender,
            profile_image_url=self.profile_image_url,
        )
