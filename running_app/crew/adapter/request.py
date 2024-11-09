from pydantic import BaseModel
from uuid import UUID
import uuid
from running_app.crew.application.invite_command import InviteCommand


class CreateCrewRequest(BaseModel):
    """Create crew request."""

    crew_name: str


class InviteUserReq(BaseModel):
    invitee_phone: str
