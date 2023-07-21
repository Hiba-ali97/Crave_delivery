from sqlalchemy import types,Column,func
from app.core.config import Base
from pydantic import BaseModel

class Resturant(Base):
    __tablename__ = 'resturant'

    id_resturant=Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    name=Column(types.VARCHAR(50),nullable=False)
    info=Column(types.VARCHAR(255),nullable=True)
    id_partner=Column(types.BigInteger,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class ResturantCreate(BaseModel):

    name: str
    info: str
    id_partner: int