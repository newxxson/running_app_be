from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from running_app.crew.domain.enum.status import CrewMemberStatus
from running_app.user.domain.enum.gender import Gender


class CrewInviteResponse(BaseModel):
    """크루 초대 요청을 나타내는 도메인 오브젝트입니다."""

    invitee_identifier: UUID
    user_identifier: UUID  # 초대 받는 사람
    crew_identifier: UUID  # 초대 한 크루
    invited_at: datetime
    is_deleted: bool
    member_status: CrewMemberStatus = CrewMemberStatus.PENDING

    @classmethod
    def from_domain(cls, crew_invite):
        return cls(
            invitee_identifier=crew_invite.user_identifier,
            user_identifier=crew_invite.user_identifier,
            crew_identifier=crew_invite.crew_identifier,
            invited_at=crew_invite.invited_at,
            is_deleted=crew_invite.is_deleted,
            member_status=crew_invite.member_status,
        )


class CrewMemberResponse(BaseModel):
    """크루 멤버 정보를 나타내는 도메인 오브젝트입니다."""

    identifier: UUID
    nickname: str
    gender: Gender

    @classmethod
    def from_domain(cls, crew_member):
        return cls(
            identifier=crew_member.identifier,
            nickname=crew_member.nickname,
            gender=crew_member.gender,
        )


class CrewMembersResponse(BaseModel):
    """크루 멤버들 정보를 리스트로 나타내는 도메인 오브젝트입니다."""

    members: list[CrewMemberResponse]

    @classmethod
    def from_domain(cls, crew_members):
        return cls(
            members=[CrewMemberResponse.from_domain(member) for member in crew_members]
        )


class CrewResponse(BaseModel):
    """크루 정보를 나타내는 도메인 오브젝트입니다."""

    identifier: UUID
    crew_name: str
