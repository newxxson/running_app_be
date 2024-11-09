from uuid import UUID
from injector import inject
from sqlalchemy import select
from running_app.common.database.db_context import DBContext
from running_app.user.adapter.output.persistence.entity.user_entity import UserEntity
from running_app.user.application.port.output.find_user_output import FindUserOutput
from running_app.user.application.port.output.save_user_output import SaveUserOutput
from running_app.user.domain.user import User


class UserPersistenceAdapter(FindUserOutput, SaveUserOutput):
    """User persistence adapter."""

    @inject
    def __init__(self, db_context: DBContext) -> None:
        self.db_context = db_context

    async def save_user(self, user: User) -> None:
        """Save user."""
        await self.db_context.session.merge(user)

    async def find_user_by_kakao_id(self, kakao_id: str) -> User | None:
        """Find user by kakao id."""
        statement = select(UserEntity).where(UserEntity.kakao_id == kakao_id)

        result = await self.db_context.session.execute(statement)

        user_entity = result.scalars().first()

        return user_entity.to_domain() if user_entity else None

    async def find_user_by_id(self, identifier: UUID) -> User | None:
        """Find user by id."""
        statement = select(UserEntity).where(UserEntity.identifier == identifier)

        result = await self.db_context.session.execute(statement)

        user_entity = result.scalars().first()

        return user_entity.to_domain() if user_entity else None
