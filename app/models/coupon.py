
from sqlalchemy import types,Column,func
from app.core.config import Base
from pydantic import BaseModel
from datetime import datetime

# Create the database model
class Coupon(Base):
    __tablename__ = 'coupon'

    id_coupon =Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    code=Column(types.VARCHAR,nullable=False)
    discount=Column(types.DECIMAL,nullable=False,index=True)
    expiration_date=Column(types.DateTime,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class CouponCreate(BaseModel):
    code:str
    discount:float
    expiration_date:datetime
