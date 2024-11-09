from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from running_app.crew.domain.crew_member import CrewMember
from running_app.crew.domain.enum.status import CrewMemberStatus
from running_app.user.domain.user import User


class CrewInviteResponse(BaseModel):
    """크루 초대 요청을 나타내는 도메인 오브젝트입니다."""

    invitee_identifier: UUID
    user_identifier: UUID  # 초대 받는 사람
    crew_identifier: UUID  # 초대 한 크루
    is_deleted: bool
    member_status: CrewMemberStatus = CrewMemberStatus.PENDING

    @classmethod
    def from_domain(cls, crew_invite):
        return cls(
            invitee_identifier=crew_invite.user_identifier,
            user_identifier=crew_invite.user_identifier,
            crew_identifier=crew_invite.crew_identifier,
            is_deleted=crew_invite.is_deleted,
            member_status=crew_invite.member_status,
        )


class CrewMemberResponse(BaseModel):
    """크루 멤버 정보를 나타내는 도메인 오브젝트입니다."""

    identifier: UUID
    nickname: str
    gender: str

    @classmethod
    def from_domain(cls, crew_member: CrewMember, user: User) -> "CrewMemberResponse":
        return cls(
            identifier=crew_member.identifier,
            nickname=user.nickname,
            gender=user.gender.value,
        )


class CrewMembersResponse(BaseModel):
    """크루 멤버들 정보를 리스트로 나타내는 도메인 오브젝트입니다."""

    members: list[CrewMemberResponse]

    @classmethod
    def from_domain(
        cls, members: list[tuple[CrewMember, User]]
    ) -> "CrewMembersResponse":
        return cls(
            members=[
                CrewMemberResponse.from_domain(member[0], member[1])
                for member in members
            ]
        )


class CrewResponse(BaseModel):
    """크루 정보를 나타내는 도메인 오브젝트입니다."""

    identifier: UUID
    crew_name: str


class InvitationResponse(BaseModel):
    """초대 정보를 나타내는 도메인 오브젝트입니다."""

    member_identifier: UUID
    crew_identifier: UUID
    invitee_identifier: UUID
    invited_at: datetime

    @classmethod
    def from_domain(cls, crew_member: CrewMember) -> "InvitationResponse":
        return cls(
            member_identifier=crew_member.identifier,
            crew_identifier=crew_member.crew_identifier,
            invitee_identifier=crew_member.user_identifier,
            invited_at=crew_member.joined_at,
        )
