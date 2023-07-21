
from sqlalchemy import types,Column,func
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class Statement(Base):
    __tablename__ = 'statement'

    id_statement =Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_resturant=Column(types.BigInteger,nullable=False)
    amount=Column(types.DECIMAL,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class StatementCreate(BaseModel):
    id_resturant:int
    amount:float
