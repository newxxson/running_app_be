

import abc
import contextlib
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession


class DBContext(abc.ABC):
    """Database context interface."""

    @contextlib.asynccontextmanager
    @abc.abstractmethod
    def begin_transaction(self, *, read_only: bool) -> AsyncIterator[None]:
        """트랜잭션을 시작합니다."""

    @property
    @abc.abstractmethod
    def session(self) -> AsyncSession:
        """Context에 따른 session을 리턴합니다."""

    @abc.abstractmethod
    async def close(self) -> None:
        """Close both read and write engines."""