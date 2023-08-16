from sqlalchemy import types,Column,func
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class Rating(Base):
    __tablename__ = 'rating'

    id_rating=Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_customer=Column(types.BigInteger,nullable=False)
    id_restaurant=Column(types.BigInteger,nullable=False)
    rate=Column(types.DECIMAL,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

class RatingCreate(BaseModel):
    id_customer:int
    id_restaurant:int
    rate:float