from sqlalchemy import Column, DateTime, ForeignKey, String, func, text

from app.db.models import Base, INNER_SCHEMA, OUTER_SCHEMA


class OuterDTO(Base):
    __tablename__ = 't_outer'
    __table_args__ = {'schema': OUTER_SCHEMA, 'extend_existing': True, 'comment': '外部用'}
    '''
    table on outer schema.
    '''

    id = Column(String(32), server_default=text("uuid_generate_v4()"), primary_key=True, index=True, comment='外部用ID')
    inner_id = Column(String(32), ForeignKey(f'{INNER_SCHEMA}.m_inner.id'), nullable=False, comment='内部用ID')
    update_date = Column(DateTime, server_default=func.current_timestamp(), nullable=False, onupdate=func.current_timestamp(), comment='更新日時')
