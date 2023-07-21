
from sqlalchemy import types,Column,func
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class OrderItem(Base):
    __tablename__ = 'order_item'

    id_order_item =Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_order=Column(types.BigInteger,nullable=False)
    id_item=Column(types.BigInteger,nullable=False)
    quantity=Column(types.INTEGER,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class OrderItemCreate(BaseModel):
    id_order:int
    id_item:int
    quantity:int
