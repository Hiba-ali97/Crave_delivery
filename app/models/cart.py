
from sqlalchemy import types,Column,func
from app.core.config import Base
from pydantic import BaseModel
# Create the database model
class Cart(Base):
    __tablename__ = 'cart'

    id_cart =Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_customer=Column(types.BigInteger,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class CartCreate(BaseModel):
    id_customer:int