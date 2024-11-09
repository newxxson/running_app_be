from datetime import datetime
from injector import inject
from running_app.crew.adapter.crew_repository import CrewRepository
from running_app.crew.application.invite_usecase import InviteUseCase
from running_app.crew.application.invite_command import InviteCommand
from running_app.crew.application.accept_invite_command import AcceptInviteCommand
from running_app.crew.adapter.response import AcceptInviteResponse
from running_app.crew.domain.crew_member import CrewMember
from running_app.crew.domain.enum.role import CrewRole
from running_app.crew.domain.enum.status import Status

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

        crew = await self.crew_repository.find_by_id(invite_command.crew_identifier) # crew_identifier로 크루 조회
        if not crew:
            raise ValueError("Crew not found")
            
        is_member = any(member.user_identifier == invite_command.current_user_id and not member.is_deleted for member in crew.members)
        if not is_member:
            raise ValueError("Only crew members can invite users")
        
        crew_member = CrewMember( # 이거를 그냥 멤버에 바로 넣고 status를 PENDING으로 설정
            user_identifier=invite_command.invitee_identifier,
            crew_identifier=crew.identifier,
            joined_at=datetime.now(),
            role=CrewRole.MEMBER,
            status=Status.PENDING,
            is_deleted=False
        )
        
        await self.crew_repository.create_member(crew_member)
        return CrewInviteResponse.from_domain(crew_member)
        

    async def accept_invite(
        self, command: AcceptInviteCommand
    ) -> AcceptInviteResponse:
        """크루 초대를 수락하는 서비스 함수입니다."""

        invite = await self.crew_repository.find_invite_by_id(command.request_identifier) # request_identifier로 초대 조회
        if not invite:
            raise ValueError("Crew invite not found")
        
        if invite.invitee_identifier != command.user_identifier:
            raise ValueError("User does not match invite")
        
        invite.status = "ACCEPTED"

        await self.crew_repository.update_member(invite.crew_identifier, invite.invitee_identifier) # 크루 멤버 업데이트
        
        return AcceptInviteResponse(
            request_identifier=invite.identifier,
            user_identifier=invite.invitee_identifier,
            crew_identifier=invite.crew_identifier,
            accepted_at=datetime.now()
        )
