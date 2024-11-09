from running_app.common.property.base import BaseProperty


class _RedisProperty(BaseProperty):
    """Redis property."""

    redis_service_host: str
    redis_service_port: int
    redis_service_db: int


redis_property = _RedisProperty()  # type: ignore
