from uuid import UUID
import msgspec


class SearchPathQuery(msgspec.Struct):
    """Query path command."""

    path_identifier: UUID

    cursor_sequence: int

    limit: int
