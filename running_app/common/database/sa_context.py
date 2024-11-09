import asyncio
import contextlib
from contextvars import ContextVar
import json
from typing import Any, AsyncIterator
from injector import inject
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_scoped_session,
    async_sessionmaker,
    AsyncSession,
)

from running_app.common.database.db_context import DBContext
from running_app.common.exception.business_exception import BusinessException
from running_app.common.log import logger
from running_app.common.property.database import database_property

NOTSET = "NOTSET"
READ = "READ"
WRITE = "WRITE"


class AsyncSQLAlchemy:
    """비동기 SQLAlchemy 클래스입니다."""

    @inject
    def __init__(self) -> None:
        options: dict[str, Any] = {"pool_pre_ping": True}
        options["json_serializer"] = lambda x: json.dumps(x, ensure_ascii=False)

        read_url = f"postgresql+asyncpg://{database_property.db_read_username}:{database_property.db_read_password}@{database_property.db_read_host}:{database_property.db_read_port}/{database_property.db_read_name}"
        master_url = f"postgresql+asyncpg://{database_property.db_username}:{database_property.db_password}@{database_property.db_host}:{database_property.db_port}/{database_property.db_name}"
        self.read_engine = create_async_engine(read_url, **options)
        self.master_engine = create_async_engine(master_url, **options)

        self.read_session_factory = async_sessionmaker(
            bind=self.read_engine, expire_on_commit=False
        )
        self.master_session_factory = async_sessionmaker(
            bind=self.master_engine, expire_on_commit=False
        )

        self.read_scoped_session_factory = async_scoped_session(
            self.read_session_factory,
            scopefunc=asyncio.current_task,
        )
        self.master_scoped_session_factory = async_scoped_session(
            self.master_session_factory,
            scopefunc=asyncio.current_task,
        )

    async def remove_session(
        self,
    ) -> None:
        """Remove sessions for both read and write engines."""
        await self.master_scoped_session_factory.remove()
        await self.read_scoped_session_factory.remove()

    async def dispose_engines(self) -> None:
        """Dispose both read and write engines."""
        await self.read_engine.dispose()
        await self.master_engine.dispose()


class AsyncSQLAlchemyContext(DBContext):
    """비동기 SQLAlchemy 컨텍스트 클래스입니다."""

    @inject
    def __init__(self, async_sa: AsyncSQLAlchemy) -> None:
        self.read_only = ContextVar(
            "read_only", default=NOTSET
        )  # 트랜잭션별 session context
        self.async_sa = async_sa

    @contextlib.asynccontextmanager
    async def begin_transaction(self, *, read_only: bool) -> AsyncIterator[None]:
        """트랜잭션의 타입을 지정하고 트랜잭션을 시작합니다.

        트랜잭션이 중첩으로 열렸을경우 나중에 열린 트랜잭션들은 제일 먼저 생긴 트랜잭션의 타입을 따라갑니다.
        """
        if self.read_only.get() == NOTSET:
            if read_only is True:
                self.read_only.set(READ)
            else:
                self.read_only.set(WRITE)

        if self.session.in_transaction():
            yield None
        else:
            async with self.session.begin():
                try:
                    yield None
                    if self.read_only.get() == WRITE:
                        await self.session.commit()
                except BusinessException:  # 비즈니스 익셉션은 글로벌 핸들러에서 따로 남기므로 추가로 남기지 않습니다.
                    raise
                except Exception:
                    logger.exception("Error in AsyncSAContext")
                    raise
                finally:
                    await self.async_sa.remove_session()
                    self.read_only.set(NOTSET)

    @property
    def session(self) -> AsyncSession:
        """Context에 따른 session을 리턴합니다."""
        if self.read_only.get() == NOTSET:
            raise BusinessException(
                status_code=500, message="Session not executed within transaction"
            )

        if self.read_only.get() == READ:
            return self.async_sa.read_scoped_session_factory()

        return self.async_sa.master_scoped_session_factory()

    async def close(self) -> None:
        """Session 연결을 종료합니다."""
        await self.async_sa.dispose_engines()
