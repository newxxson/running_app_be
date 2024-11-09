from typing import Annotated
from fastapi import APIRouter, Depends, Path, Response, status
from uuid import UUID
import uuid

from yaml import AnchorToken
from running_app.common.auth.jwt_token_deserializer import get_current_user
from running_app.crew.adapter.request import CreateCrewRequest, InviteUserReq
from running_app.crew.adapter.response import (
    CrewInviteResponse,
    CrewResponse,
    InvitationResponse,
)
from running_app.crew.application.create_crew_usecase import CreateCrewUseCase
from running_app.crew.application.invite_command import InviteCommand
from running_app.crew.application.invite_usecase import InviteUseCase
from running_app.crew.application.accept_invite_command import AcceptInviteCommand
from running_app.crew.application.accept_invite_usecase import AcceptInviteUseCase
from running_app.crew.application.get_crew_members_usecase import GetCrewMembersUseCase
from running_app.crew.application.get_crew_members_command import GetCrewMembersCommand
from running_app.crew.adapter.response import CrewMembersResponse
from running_app.common.di import on
from running_app.crew.application.query_crew_members_usecase import (
    QueryCrewMembersUseCase,
)
from running_app.crew.domain.enum.status import CrewMemberStatus


crew_router = APIRouter()


@crew_router.post("/crews/{crew_identifier}/member", status_code=status.HTTP_200_OK)
async def invite_user(
    request: InviteUserReq,
    invite_usecase: Annotated[InviteUseCase, Depends(on(InviteUseCase))],
    current_user_id: UUID = Depends(get_current_user),
    crew_identifier: UUID = Path(),
) -> Response:
    """크루에 사용자를 초대합니다."""

    command = InviteCommand(
        invitee_phone=request.invitee_phone,
        crew_identifier=crew_identifier,
        current_user_id=current_user_id,
    )
    await invite_usecase.invite(command)

    return Response(status_code=status.HTTP_200_OK)


@crew_router.put("/crews/{crew_identifier}/member/{member_identifier}")
async def accept_invite(
    member_identifier: UUID,
    crew_identifier: UUID,
    accept_invite_usecase: Annotated[
        AcceptInviteUseCase, Depends(on(AcceptInviteUseCase))
    ],
    current_user_id: UUID = Depends(get_current_user),
) -> Response:
    command = AcceptInviteCommand(
        member_identifier=member_identifier, user_identifier=current_user_id
    )
    return await accept_invite_usecase.accept_invite(command)


@crew_router.get("/crews/{crew_identifier}/members")
async def get_crew_members(
    get_crew_members_usecase: Annotated[
        GetCrewMembersUseCase, Depends(on(GetCrewMembersUseCase))
    ],
    current_user_id: UUID = Depends(get_current_user),
    crew_identifier: UUID = Path(),
) -> CrewMembersResponse:
    command = GetCrewMembersCommand(
        crew_identifier=crew_identifier,
    )
    return await get_crew_members_usecase.get_crew_members(command)


@crew_router.post("/crews")
async def create_crew(
    create_crew_request: CreateCrewRequest,
    create_crew_usecase: Annotated[CreateCrewUseCase, Depends(on(CreateCrewUseCase))],
) -> CrewResponse:
    """"""
    crew = await create_crew_usecase.create_crew(
        crew_name=create_crew_request.crew_name
    )
    return CrewResponse(
        identifier=crew.identifier,
        crew_name=crew.crew_name,
    )


@crew_router.get("/crews/invitations")
async def get_invitations(
    query_crew_members_usecase: Annotated[
        QueryCrewMembersUseCase, Depends(on(QueryCrewMembersUseCase))
    ],
    current_user_id: UUID = Depends(get_current_user),
) -> list[InvitationResponse]:
    """Get invitations."""
    crew_members = (
        await query_crew_members_usecase.find_crew_member_by_user_id_and_status(
            user_identifier=current_user_id,
            status=CrewMemberStatus.PENDING,
        )
    )
    return [InvitationResponse.from_domain(crew_member) for crew_member in crew_members]
