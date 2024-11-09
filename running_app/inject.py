from injector import Binder, Injector, inject
from jinja2 import ModuleLoader

from running_app.common.database.db_context import DBContext
from running_app.common.database.sa_context import AsyncSQLAlchemyContext


def service_configure(binder: Binder) -> None:  # noqa: PLR0915
    binder.bind(DBContext, to=AsyncSQLAlchemyContext)


injector = Injector(modules=[service_configure])
