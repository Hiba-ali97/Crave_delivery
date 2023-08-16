
from sqlalchemy import types,Column,func
from sqlalchemy.dialects.mysql import TINYINT
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class Customer(Base):
    __tablename__ = 'customer'

    id_customer = Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_credit = Column(types.BigInteger,nullable=True)
    name = Column(types.VARCHAR(50),nullable=False)
    password = Column(types.VARCHAR(100),nullable=False)
    phone_number=Column(types.VARCHAR(20),nullable=False,unique=True)
    vip=Column(TINYINT(1),nullable=False)
    location_lat=Column(types.DECIMAL,nullable=False)
    location_lng=Column(types.DECIMAL,nullable=False)
    location_address=Column(types.VARCHAR,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)


class CustomerCreate(BaseModel):
    id_credit: int
    name: str
    password: str
    phone_number: str
    vip: int
    location_lat: float
    location_lng: float
    location_address: str
