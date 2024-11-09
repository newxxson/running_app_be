import abc

from running_app.crew.application.delete_member_command import DeleteMemberCommand


class DeleteMemberUseCase(abc.ABC):
    
    @abc.abstractmethod
    async def delete_member(self, command: DeleteMemberCommand) -> None:
        """Delete member."""
    