from sqlalchemy import Column, func, DateTime, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class StatesModel(Base):

    __tablename__ = 'states'

    state_id=Column(Integer, primary_key=True)
    name=Column(String(250), nullable=True)
    code_dane=Column(String(250), nullable=True)
    country_id=Column(Integer)
    active=Column(Integer, nullable=True, default=str(1))
    created_at=Column(DateTime, nullable=True, default=func.current_timestamp())
    updated_at=Column(DateTime, nullable=True, default=func.current_timestamp())

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
