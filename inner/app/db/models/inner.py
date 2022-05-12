from sqlalchemy import (Column, DateTime, String,
                        func, text)

from app.db.models import Base
from app.db.migration.env import INNER_SCHEMA


class InnerDTO(Base):
    __tablename__ = 'm_inner'
    __table_args__ = {'schema': INNER_SCHEMA, 'extend_existing': True, 'comment': 'for inner'}
    '''
    table on inner schema
    '''
    id = Column(String(32), server_default=text("uuid_generate_v4()"), primary_key=True, index=True, comment='内部用ID')
    update_date = Column(DateTime, server_default=func.current_timestamp(), nullable=False, onupdate=func.current_timestamp(), comment='更新日時')
