
from sqlalchemy import types,Column,func
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class OrderItemOption(Base):
    __tablename__ = 'order_item_option'

    id_order_item_option=Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_order_item=Column(types.BigInteger,nullable=False)
    id_option=Column(types.BigInteger,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class OrderItemOptionCreate(BaseModel):
    id_order_item:int
    id_option:int