
from sqlalchemy import types,Column,func
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class ResturantCoupon(Base):
    __tablename__ = 'resturant_coupon'

    id_resturant_coupon =Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_resturant=Column(types.BigInteger,nullable=False)
    id_coupon=Column(types.BigInteger,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class ResturantCouponCreate(BaseModel):
    id_resturant:int
    id_coupon:int