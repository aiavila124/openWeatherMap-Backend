from sqlalchemy import Column, func, String, Integer, DateTime, BLOB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class IconsModel(Base):

    __tablename__ = 'icons'

    icon_id=Column(Integer, primary_key=True)
    description=Column(String(50), nullable=True)
    path=Column(String(250), nullable=True)
    code=Column(String(50), nullable=True)
    active=Column(Integer, nullable=True, default=str(1))
    created_at=Column(DateTime, nullable=True, default=func.current_timestamp())
    updated_at=Column(DateTime, nullable=True, default=func.current_timestamp())

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


