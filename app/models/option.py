
from sqlalchemy import types,Column,func
from sqlalchemy.dialects.mysql import TINYINT
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class Option(Base):
    __tablename__ = 'option'

    id_option=Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_item=Column(types.BigInteger)
    name=Column(types.VARCHAR(100),nullable=False)
    is_extra=Column(TINYINT(1),nullable=False)
    price=Column(types.DECIMAL,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class OptionCreate(BaseModel):
    id_item:int
    name:str
    is_extra:int
    price:float