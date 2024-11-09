from running_app.common.property.base import BaseProperty


class _KakaoProperty(BaseProperty):
    """Kakao property."""

    kakao_api_url: str


kakao_property = _KakaoProperty()  # type: ignore[call-arg]
