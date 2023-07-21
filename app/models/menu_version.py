
from sqlalchemy import types,Column,func
from sqlalchemy.dialects.mysql import TINYINT
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class MenuVersion(Base):
    __tablename__ = 'menu_version'

    id_menu_version=Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_menu=Column(types.BigInteger)
    is_active=Column(TINYINT(1),nullable=False)
    version=Column(types.Integer,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class MenuVersionCreate(BaseModel):
    id_menu:int
    is_active:int
    version:int