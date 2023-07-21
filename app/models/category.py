
from sqlalchemy import types,Column,func
from pydantic import BaseModel
from app.core.config import Base
# Create the database model
class Category(Base):
    __tablename__ = 'category'

    id_category =Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_menu=Column(types.BigInteger,nullable=False)
    name=Column(types.VARCHAR(50),nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class CategoryCreate(BaseModel):
    id_menu:int
    name:str
