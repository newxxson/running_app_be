from pydantic import BaseModel
from uuid import UUID

from running_app.crew.application.invite_command import InviteCommand


class InviteUserRequest(BaseModel):
    user_identifier: UUID
    crew_identifier: UUID
    current_user_id: UUID
    def to_command(self) -> InviteCommand:
        return InviteCommand(
            user_identifier=self.user_identifier,
            crew_identifier=self.crew_identifier,
            current_user_id=self.current_user_id,
        )
    

class InviteUserReq(BaseModel):
    user_identifier: UUID