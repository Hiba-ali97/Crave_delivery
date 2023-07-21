from sqlalchemy import types,Column,func,UniqueConstraint
from app.core.config import Base
from pydantic import BaseModel

# Create the database model
class CustomerCredit(Base):
    __tablename__ = 'customer_credit'

    id_customer_credit =Column(types.BigInteger, primary_key=True, index=True,autoincrement=True,nullable=False)
    id_customer=Column(types.BigInteger,nullable=False)
    id_credit =Column(types.BigInteger,nullable=False)
    created_at=Column(types.DateTime , server_default=func.current_timestamp(), index=True,nullable=False)
    updated_at=Column(types.DateTime , server_default=func.current_timestamp(),onupdate=func.current_timestamp(),nullable=False)

    __table_args__ = (
        UniqueConstraint('id_customer', 'id_credit', name='uq_customer_credit'),
    )


class CustomerCreditCreate(BaseModel):
    id_customer:int
    id_credit:int

