from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class URL(Base):
    __tablename__ = 'urls'
    
    id = Column(Integer, primary_key=True)
    original_url = Column(String(2048), nullable=False)
    short_code = Column(String(10), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    clicks = Column(Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_code': self.short_code,
            'created_at': self.created_at.isoformat(),
            'clicks': self.clicks
        }

def init_db(database_url='sqlite:///urls.db'):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
