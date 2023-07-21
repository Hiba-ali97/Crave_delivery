
from sqlalchemy import types,Column,func
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class Item(Base):
    __tablename__ = 'item'

    id_item =Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_category=Column(types.BigInteger,nullable=False)
    name=Column(types.VARCHAR(50),nullable=False)
    description=Column(types.VARCHAR(),nullable=True)
    image=Column(types.VARCHAR,nullable=True)
    price=Column(types.DECIMAL,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class ItemCreate(BaseModel):
    id_category:int
    name:str
    description:str
    image:str
    price:float
