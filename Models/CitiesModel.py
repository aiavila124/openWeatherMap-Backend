from sqlalchemy import Column, func, String, Integer, DateTime, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class CitiesModel(Base):

    __tablename__ = 'cities'

    city_id=Column(Integer, primary_key=True)
    name=Column(String(50), nullable=True)
    code_dane=Column(String(50), nullable=True)
    lng=Column(DECIMAL(20,6), nullable=True)
    lat=Column(DECIMAL(20,6), nullable=True)
    state_id=Column(Integer)
    active=Column(Integer, nullable=True, default=str(1))
    created_at=Column(DateTime, nullable=True, default=func.current_timestamp())
    updated_at=Column(DateTime, nullable=True, default=func.current_timestamp())

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
