from sqlalchemy.orm import declarative_base
from app.db.migration.config import DBSettings

Base = declarative_base()

INNER_SCHEMA: str = DBSettings().inner_db_schema
OUTER_SCHEMA: str = DBSettings().outer_db_schema
