from sqlalchemy import types,Column,func
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class Partner(Base):
    __tablename__ = 'partner'

    id_partner=Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    name=Column(types.VARCHAR(50),nullable=False)
    password=Column(types.VARCHAR(100),nullable=False)
    phone_number=Column(types.VARCHAR(20),nullable=False,unique=True)
    email=Column(types.VARCHAR,nullable=False,unique=True)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class PartnerCreate(BaseModel):
    name:str
    password:str
    phone_number:str
    email:str