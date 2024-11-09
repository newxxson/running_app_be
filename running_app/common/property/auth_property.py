from running_app.common.property.base import BaseProperty


class _AuthProperty(BaseProperty):
    """Auth property."""

    jwt_secret_key: str

    access_token_expiration_minutes: int
    refresh_token_expiration_days: int

    algorithm: str


auth_property = _AuthProperty()  # type: ignore
