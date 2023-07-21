
from sqlalchemy import types,Column,func
from sqlalchemy.dialects.mysql import TINYINT
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class Order(Base):
    __tablename__ = 'order'

    id_order =Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_customer=Column(types.BigInteger,nullable=False)
    id_cart=Column(types.BigInteger,nullable=False)
    id_outlet=Column(types.BigInteger,nullable=False)
    id_statement=Column(types.BigInteger,nullable=False)
    payment_done=Column(TINYINT(1),nullable=False)
    price=Column(types.DECIMAL,nullable=False)
    statement=Column(TINYINT(1),nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class OrderCreate(BaseModel):
    id_customer:int
    id_cart:int
    id_outlet:int
    id_statement:int
    payment_done:int
    price:float
    statement:int
