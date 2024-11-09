from running_app.common.property.base import BaseProperty


class _PathProperty(BaseProperty):
    """Path property."""

    average_speed: float


path_property = _PathProperty()  # type: ignore
