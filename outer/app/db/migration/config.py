import logging
import os
import sys
from typing import Optional

from app.db.migration.logging import InterceptHandler
from loguru import logger
from pydantic import BaseSettings
from pydantic.networks import EmailStr


def _get_cfg_name() -> str:
    if 'ENV' in os.environ:
        return f'app/.{os.environ["ENV"]}.env'
    else:
        return 'app/.env'


def _is_debug() -> bool:
    if os.getenv('ENV') == 'docker':
        return True
    elif os.getenv('DEPLOY_ENV') == 'dev':
        return True
    else:
        return False


class GlobalSettings(BaseSettings):
    project_name: str = 'Parts Management'
    version: str = '0.0.1'
    is_aws: bool = _is_aws()
    debug: bool = _is_debug()


class DBSettings(BaseSettings):
    database: str
    db_user: str
    password: str
    host: str
    port: int
    db_name: str
    min_connections_count: int
    max_connections_count: int
    inner_db_schema: str
    outer_db_schema: str

    class Config:
        env_file = _get_cfg_name()


class LoggingSettings(BaseSettings):
    logging_level: int = logging.DEBUG
    loggers = ('uvicorn.asgi', 'uvicorn.access')


"""
logger configuration
"""
logging_settings = LoggingSettings()
global_settings = GlobalSettings()

# logging level: depends on whether debug or not
logging_settings.logging_level = logging.DEBUG\
    if global_settings.debug else logging.INFO

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in logging_settings.loggers:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [
        InterceptHandler(level=logging_settings.logging_level)]

logger.configure(handlers=[
    {'sink': sys.stderr, 'level': logging_settings.logging_level}])
