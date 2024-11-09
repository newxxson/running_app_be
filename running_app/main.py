from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator

from fastapi.concurrency import run_in_threadpool
from running_app.common.cache.cache import CacheManager
from running_app.common.database.sa_context import AsyncSQLAlchemy
from running_app.user.adapter.input.web.user_controller import user_router
from running_app.path.adapter.input.web.path_controller import path_router
from running_app.running.run.adapter.input.web.run_controller import run_router
from running_app.running.running_state.adapter.input.web.running_state_controller import (
    running_state_router,
)
from fastapi.middleware.cors import CORSMiddleware
from running_app.common.log import logger
from running_app.crew.adapter.crew_controller import crew_router

from fastapi import APIRouter, Depends, FastAPI
from running_app.common.di import injector, on


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
# Define allowed origins for CORS. Use ["*"] to allow all origins.
origins = [
    "http://localhost:3000",  # Example: frontend on a different port
]

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origins allowed to access the API
    allow_credentials=True,  # Allows cookies to be sent with requests
    allow_methods=["*"],  # HTTP methods allowed (GET, POST, etc.)
    allow_headers=["*"],  # Headers allowed in requests
)
app.include_router(crew_router)


main_router = APIRouter()


@main_router.get("/")
async def test_redis(
    cache_manger: Annotated[CacheManager, Depends(on(CacheManager))],
) -> str:
    await cache_manger.set_cache("test", {"test": "test"})
    result = await cache_manger.get_cache("test")
    logger.info(result)
    return "test"


app.include_router(main_router)
