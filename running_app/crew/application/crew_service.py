from uuid import UUID
from datetime import datetime
from injector import inject
from running_app.crew.adapter.crew_repository import CrewRepository
from running_app.crew.application.invite_usecase import InviteUseCase
from running_app.crew.application.invite_command import InviteCommand

from running_app.crew.domain.crew_invite import CrewInvite
from adapter.response import CrewInviteResponse
from running_app.common.database.db_context import DBContext


class CrewService(InviteUseCase):
    """Crew service."""

    @inject
    def __init__(
        self,
        db_context: DBContext,
        crew_repository: CrewRepository
    ) -> None:
        self.db_context = db_context
        self.crew_repository = crew_repository

    async def service_invite_user(
        self, invite_command: InviteCommand
    ) -> CrewInviteResponse:
        """크루에 사용자를 초대하는 서비스 함수입니다."""

        crew = await self.crew_repository.find_by_id(invite_command.crew_identifier)
        if not crew:
            raise ValueError("Crew not found")
            
        is_member = any(member.user_identifier == invite_command.current_user_id and not member.is_deleted for member in crew.members)
        if not is_member:
            raise ValueError("Only crew members can invite users")
        
        crew_invite = CrewInvite(
            request_identifier=UUID(),
            crew_identifier=crew.identifier,
            user_identifier=invite_command.user_identifier,
            invited_at=datetime.now(),
            status="PENDING",
            is_deleted=False
        )
        
        saved_invite = await self.crew_repository.save_invite(crew_invite)
        return CrewInviteResponse.from_domain(saved_invite)
        
