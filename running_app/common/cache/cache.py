import abc


class CacheManager(abc.ABC):
    """레디스 매니저 추상 클래스."""

    @abc.abstractmethod
    def start(self) -> None:
        """레디스 매니저를 시작합니다."""

    @abc.abstractmethod
    def close(self) -> None:
        """레디스 연결을 종료합니다."""

    @abc.abstractmethod
    async def set_cache(self, key: str, mapping: dict) -> None:
        """캐시를 생성합니다."""

    @abc.abstractmethod
    async def delete_cache(self, key: str) -> None:
        """캐시를 무효화합니다."""

    @abc.abstractmethod
    async def get_cache(self, key: str) -> dict | None:
        """Key에 따라 캐시를 조회합니다."""
