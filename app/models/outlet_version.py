
from sqlalchemy import types,Column,func
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class OutletVersion(Base):
    __tablename__ = 'outlet_version'

    id_outlet_version =Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_outlet=Column(types.BigInteger,nullable=False)
    id_menu=Column(types.BigInteger,nullable=False)
    version=Column(types.Integer,nullable=False)
    commission_fee=Column(types.DECIMAL,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class OutletVersionCreate(BaseModel):
    id_outlet:int
    id_menu:int
    version:int
    commission_fee: float
