from sqlalchemy import types,Column,func
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class Menu(Base):
    __tablename__ = 'menu'
    id_menu =Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_resturant=Column(types.BigInteger,nullable=False)
    name=Column(types.VARCHAR(100),nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class MenuCreate(BaseModel):
    id_resturant:int
    name:str
