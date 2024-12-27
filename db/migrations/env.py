import asyncio
from logging.config import fileConfig

from sqlalchemy import Connection
from sqlalchemy import pool

from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config

from bot.constants.env import DB_URL
from db.models.user import TGUser
from db.models.form import FormDB

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = TGUser.metadata

config.set_main_option("sqlalchemy.url", DB_URL)


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
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    raise Exception("Offline mode is not supported")
else:
    run_migrations_online()
