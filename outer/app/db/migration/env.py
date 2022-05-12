from logging.config import fileConfig

from loguru import logger

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.schema import CreateSchema
from app.db.migration.config import DBSettings

from app.db.models import (Base, outer)

INNER_SCHEMA: str = DBSettings().inner_db_schema
OUTER_SCHEMA: str = DBSettings().outer_db_schema

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(str(config.config_file_name))

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

settings = DBSettings()
__uri = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
    settings.db_user,
    settings.password,
    settings.host,
    settings.port,
    settings.db_name
)
config.set_main_option('sqlalchemy.url', __uri)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # 追加
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    cmd_opts = config.cmd_opts
    if cmd_opts:
        cmd = cmd_opts.cmd[0]  # ignore: type
        cmd_name = getattr(cmd, '__name__')
    else:
        cmd_name = ""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        if cmd_name == 'upgrade':
            connection.execute(f"set search_path to {OUTER_SCHEMA}, public")
            version_table_schema = OUTER_SCHEMA
        else:
            connection.execute(f"set search_path to {OUTER_SCHEMA}")
            version_table_schema = None

        # スキーマ存在確認
        if not connection.dialect.has_schema(connection, OUTER_SCHEMA):  # type: ignore
            connection.execute(CreateSchema(OUTER_SCHEMA))
            exist_schema = False
        else:
            exist_schema = True
        logger.info(exist_schema)
        # 拡張機能追加
        connection.execute("create extension IF NOT EXISTS pgcrypto")
        connection.execute('create extension IF NOT EXISTS "uuid-ossp"')

        # make use of non-supported SQLAlchemy attribute to ensure
        # the dialect reflects tables in terms of the current tenant name
        connection.dialect.default_schema_name = OUTER_SCHEMA

        def include_object(object, name, type_, reflected, compare_to):
            if type_ == "table" and (object.schema != OUTER_SCHEMA):  # type: ignore
                return False
            else:
                return True

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=version_table_schema,
            compare_type=True,
            include_schemas=True,
            include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
