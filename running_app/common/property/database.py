from running_app.common.property.base import BaseProperty


class _DataBaseProperty(BaseProperty):
    """Database property."""

    db_host: str
    db_port: int
    db_name: str

    db_username: str
    db_password: str

    db_read_host: str
    db_read_port: int
    db_read_username: str
    db_read_password: str
    db_read_name: str


database_property = _DataBaseProperty()  # type: ignore
