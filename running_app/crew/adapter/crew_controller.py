from typing import Annotated
from fastapi import APIRouter, Depends, Path, Response, status
from uuid import UUID

from running_app.common.auth.jwt_token_deserializer import get_current_user
from request import InviteUserReq
from response import CrewInviteResponse
from running_app.crew.application.invite_command import InviteCommand
from running_app.crew.application.invite_usecase import InviteUseCase
from running_app.crew.application.accept_invite_command import AcceptInviteCommand
from running_app.crew.application.accept_invite_usecase import AcceptInviteUseCase

from running_app.common.di import on


crew_router = APIRouter()


@crew_router.post(
    "/crews/{crew_identifier}/member", 
    status_code=status.HTTP_200_OK
)
async def invite_user(
    invite_usecase: Annotated[InviteUseCase, Depends(on(InviteUseCase))],
    current_user_id: UUID = Depends(get_current_user),
    crew_identifier: UUID = Path(),
    request: InviteUserReq = Depends(),
) -> Response:
    """크루에 사용자를 초대합니다."""

    command = InviteCommand(
        invitee_identifier=request.invitee_identifier,
        crew_identifier=crew_identifier,
        current_user_id=current_user_id,
    )
    await invite_usecase.invite(command)

    return Response(status_code=status.HTTP_200_OK)



@crew_router.put("/crews/{crew_identifiers}/member/{member_identifier}")
async def accept_invite(
    member_identifier: UUID,
    crew_identifier: UUID,
    accept_invite_usecase: Annotated[AcceptInviteUseCase, Depends(on(AcceptInviteUseCase))],
    current_user_id: UUID = Depends(get_current_user),
) -> CrewInviteResponse:

    command = AcceptInviteCommand(
        member_identifier=member_identifier,
        user_identifier=current_user_id
    )
    crew_invite = await accept_invite_usecase.accept_invite(command)
    return CrewInviteResponse.from_domain(crew_invite)

