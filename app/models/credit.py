
from sqlalchemy import types,Column,func
from app.core.config import Base
from pydantic import BaseModel
from datetime import datetime
# Create the database model
class Credit(Base):
    __tablename__ = 'credit'

    id_credit_card =Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    cardholder_name=Column(types.VARCHAR,nullable=False)
    card_number =Column(types.VARCHAR(20),nullable=False)
    expiration_date=Column(types.DateTime,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class CreditCreate(BaseModel):
    cardholder_name:str
    card_number:str
    expiration_date:datetime

