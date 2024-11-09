from datetime import datetime
from injector import inject

from fastapi import Response, status

from running_app.crew.adapter.crew_repository import CrewRepository
from running_app.crew.application.accept_invite_usecase import AcceptInviteUseCase
from running_app.crew.application.create_crew_usecase import CreateCrewUseCase
from running_app.crew.application.invite_usecase import InviteUseCase
from running_app.crew.application.invite_command import InviteCommand
from running_app.crew.application.accept_invite_command import AcceptInviteCommand
from running_app.crew.application.get_crew_members_usecase import GetCrewMembersUseCase
from running_app.crew.application.get_crew_members_command import GetCrewMembersCommand

from running_app.crew.domain.crew import Crew
from running_app.crew.domain.crew_member import CrewMember
from running_app.crew.domain.enum.role import CrewRole
from running_app.crew.domain.enum.status import CrewMemberStatus
from running_app.crew.domain.exception.crew_not_found_exception import (
    CrewNotFoundException,
)
from running_app.crew.domain.exception.crew_member_not_found_exception import (
    CrewMemberNotFoundException,
)
from running_app.crew.adapter.response import CrewInviteResponse, CrewMembersResponse

from running_app.common.database.db_context import DBContext

import uuid


class CrewService(
    InviteUseCase, AcceptInviteUseCase, GetCrewMembersUseCase, CreateCrewUseCase
):
    """Crew service."""

    @inject
    def __init__(self, db_context: DBContext, crew_repository: CrewRepository) -> None:
        self.db_context = db_context
        self.crew_repository = crew_repository

    async def invite(self, command: InviteCommand) -> CrewInviteResponse:
        """크루에 사용자를 초대하는 서비스 함수입니다."""
        async with self.db_context.begin_transaction(read_only=False):
            crew = await self.crew_repository.find_by_id(
                command.crew_identifier
            )  # crew_identifier로 크루 조회

        if not crew:
            raise CrewNotFoundException()

        async with self.db_context.begin_transaction(read_only=True):
            is_member = await self.crew_repository.find_member_by_user_id_and_crew_id(
                user_identifier=command.current_user_id, crew_identifier=crew.identifier
            )

        if not is_member:
            raise CrewMemberNotFoundException()

        crew_member = (
            CrewMember(  # 이거를 그냥 멤버에 바로 넣고 status를 PENDING으로 설정
                identifier=uuid.uuid4(),
                user_identifier=command.user_identifier,
                crew_identifier=crew.identifier,
                joined_at=datetime.now(),
                role=CrewRole.MEMBER,
                member_status=CrewMemberStatus.PENDING,
                is_deleted=False,
            )
        )

        async with self.db_context.begin_transaction(read_only=False):
            await self.crew_repository.create_member(crew_member)
        return CrewInviteResponse.from_domain(crew_member)

    async def accept_invite(self, command: AcceptInviteCommand) -> Response:
        """크루 초대를 수락하는 서비스 함수입니다."""
        async with self.db_context.begin_transaction(read_only=False):
            member = await self.crew_repository.find_member_by_id(
                command.member_identifier
            )  # member_identifier로 멤버 조회

        if not member:
            raise ValueError("Crew member not found")

        if member.user_identifier != command.user_identifier:
            raise ValueError("User does not match invite")

        member.member_status = CrewMemberStatus.ACTIVE

        async with self.db_context.begin_transaction(read_only=False):
            await self.crew_repository.update_member(
                member.crew_identifier, member.user_identifier
            )  # 크루 멤버 업데이트

        return Response(status_code=status.HTTP_200_OK)

    async def get_crew_members(
        self, command: GetCrewMembersCommand
    ) -> CrewMembersResponse:
        """크루 멤버들을 조회하는 서비스 함수입니다."""

        if not command.crew_identifier:
            raise CrewNotFoundException()

        async with self.db_context.begin_transaction(read_only=True):
            members = await self.crew_repository.find_members_by_crew_id(
                command.crew_identifier
            )

        return CrewMembersResponse.from_domain(members)

    async def create_crew(self, crew_name: str) -> Crew:
        """크루를 생성하는 서비스 함수입니다."""
        crew = Crew(
            identifier=uuid.uuid4(),
            crew_name=crew_name,
        )

        async with self.db_context.begin_transaction(read_only=False):
            await self.crew_repository.create(crew)

        return crew

    # current_user_id로 크루 조회
    # join으로 User 같이 해서 CrewMemberResponse로 반환
