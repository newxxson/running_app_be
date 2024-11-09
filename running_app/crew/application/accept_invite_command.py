from uuid import UUID
from dataclasses import dataclass

@dataclass
class AcceptInviteCommand:
    invite_identifier: UUID
    user_identifier: UUID 