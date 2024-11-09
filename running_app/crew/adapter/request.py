from pydantic import BaseModel


class CreateCrewRequest(BaseModel):
    """Create crew request."""

    crew_name: str


class InviteUserReq(BaseModel):
    invitee_phone: str
