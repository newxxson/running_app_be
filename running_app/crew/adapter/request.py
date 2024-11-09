from pydantic import BaseModel
from uuid import UUID

from running_app.crew.application.invite_command import InviteCommand


class InviteUserRequest(BaseModel):
    invitee_identifier: UUID
    crew_identifier: UUID
    current_user_id: UUID
    def to_command(self) -> InviteCommand:
        return InviteCommand(
            invitee_identifier=self.invitee_identifier,
            crew_identifier=self.crew_identifier,
            current_user_id=self.current_user_id,
        )
    

class InviteUserReq(BaseModel):
    invitee_identifier: UUID