
from sqlalchemy import types,Column,func
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class Outlet(Base):
    __tablename__ = 'outlet'

    id_outlet  =Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_restaurant=Column(types.BigInteger,nullable=False)
    phone_number=Column(types.Integer,nullable=False,unique=True)
    location_lat=Column(types.DECIMAL,nullable=False)
    location_lng=Column(types.DECIMAL,nullable=False)
    location_address=Column(types.VARCHAR,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class OutletCreate(BaseModel):
    id_restaurant:int
    phone_number: int
    location_lat: float
    location_lng: float
    location_address: str
