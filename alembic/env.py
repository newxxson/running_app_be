import asyncio
import importlib
from logging.config import fileConfig
import os

from sqlalchemy.engine import Connection

from sqlalchemy import pool
from pathlib import Path
from alembic import context  # type: ignore[attr-defined]
from running_app.common.database.base_model import Base
from running_app.common.property.database import database_property

from sqlalchemy.ext.asyncio import async_engine_from_config


def _import_all_entities() -> None:
    """패키지명이 entity 인 파일을 전부 import 합니다.

    alembic 에서 import 가 완료된 파일만 autogenerate 를 진행하므로 entity 패키지들은 전부 import 를 진행합니다.
    """
    # 현재 스크립트의 디렉토리 (migration 디렉토리)
    current_dir = Path(__file__).resolve().parent
    # 프로젝트 루트 디렉토리로 이동
    project_root = current_dir.parent
    # 메시지 디렉토리로 이동
    analysis_service_dir = project_root / "running_app"

    for dirpath, dirnames, _ in os.walk(analysis_service_dir):
        if "entity" in dirnames:
            entity_dir = Path(dirpath) / "entity"
            for filename in entity_dir.iterdir():
                if filename.suffix == ".py" and filename.name != "__init__.py":
                    relative_path = filename.relative_to(project_root)
                    module_path = (
                        str(relative_path).replace(os.sep, ".").replace(".py", "")
                    )
                    importlib.import_module(module_path)


_import_all_entities()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# url 설정
url = f"postgresql+asyncpg://{database_property.db_username}:{database_property.db_password}@{database_property.db_host}:{database_property.db_port}/{database_property.db_name}"


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=url,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
