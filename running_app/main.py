from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi.concurrency import run_in_threadpool
from running_app.common.cache.cache import CacheManager
from running_app.common.database.db_context import DBContext
from running_app.common.database.sa_context import AsyncSQLAlchemy
from running_app.user.adapter.input.web.user_controller import user_router
from running_app.path.adapter.input.web.path_controller import path_router
from running_app.running.run.adapter.input.web.run_controller import run_router
from running_app.running.running_state.adapter.input.web.running_state_controller import (
    running_state_router,
)
from running_app.common.log import logger
from running_app.crew.adapter.crew_controller import crew_router

from fastapi import FastAPI
from running_app.common.di import injector


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:
    """FastAPI 서버가 시작되고 종료될 때 실행할 작업을 정의합니다."""
    logger.info("start fastapi server...")
    cache = injector.get(CacheManager)
    await run_in_threadpool(cache.start)

    yield

    async_sa = injector.get(AsyncSQLAlchemy)
    await async_sa.dispose_engines()

    redis_manager = injector.get(CacheManager)
    await run_in_threadpool(redis_manager.close)

    logger.info("end fastapi server...")


app = FastAPI(lifespan=lifespan)


app.include_router(user_router)
app.include_router(path_router)
app.include_router(run_router)
app.include_router(running_state_router)
app.include_router(crew_router)