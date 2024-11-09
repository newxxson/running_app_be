from typing import Awaitable
from fastapi.concurrency import run_in_threadpool
import redis
from running_app.common.cache.cache import CacheManager
from running_app.common.property.redis import redis_property
from running_app.common.log import logger


class RedisManager(CacheManager):
    """Redis cache."""

    def start(self) -> None:
        """레디스 매니저를 시작합니다."""
        try:
            self._connection_pool = redis.ConnectionPool(
                host=redis_property.redis_service_host,
                port=redis_property.redis_service_port,
                db=redis_property.redis_service_db,
            )
            self._redis = redis.Redis(connection_pool=self._connection_pool, ssl=True)
        except Exception:
            logger.critical("Couldn't connect to Redis", exc_info=True)
            raise

    def close(self) -> None:
        if self._redis is not None:
            self._redis.close()

        if self._connection_pool is not None:
            self._connection_pool.close()

    async def set_cache(self, key: str, mapping: dict) -> None:
        """키에 따라 캐시를 생성합니다."""
        mapping = self._change_to_none_safe_mapping(mapping=mapping)

        await run_in_threadpool(self._redis.hset, name=key, mapping=mapping)
        await run_in_threadpool(self._redis.expire, name=key, time=1 * 60 * 60)

    async def get_cache(self, key: str) -> dict | None:
        """키에 따라 캐시를 조회합니다."""
        cache_dict = await run_in_threadpool(self._redis.hgetall, name=key)

        if isinstance(cache_dict, Awaitable):
            raise Exception("Cache is not ready")

        return {key.decode(): value.decode() for key, value in cache_dict.items()}

    async def delete_cache(self, key: str) -> None:
        """캐시를 삭제합니다."""
        await run_in_threadpool(self._redis.delete, key)

    def _change_to_none_safe_mapping(self, mapping: dict) -> dict:
        """레디스 캐시 값으로 null이 들어가지 않도록 변환하는 function입니다."""
        safe_mapping = {}
        for k, v in mapping.items():
            if not v:
                safe_mapping[k] = ""
            else:
                safe_mapping[k] = v

        return safe_mapping
